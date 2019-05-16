package main

// hello-server.go - program to send http GET response with hostname as JSON
// the server will sense its own local IP on ifc 0 and listen on port 82 at that address.
//
// github example: https://gist.github.com/denji/12b3a568f092ab951456
//
// compile: cd ~/go/src/hello-server; go build
// command: sudo ./hello-server
//
// Name: R. Melton
// Date:  4/23/18
//
// how to get param from GET query https://golangcode.com/get-a-url-parameter-from-a-request/
// good post on JSON in http response https://medium.com/@edwardpie/parsing-json-request-body-return-json-response-with-golang-c4f862bbb19b
//
import (
	"encoding/json"
	"fmt"
	"net"
	"net/http"
	"os"
	"strconv"
	"time"
)

// GetResp json response structure; fields must be upper case
type GetResp struct {
	ResponseAt time.Time
	ReqCnt     int
	SrcIP      string
	ListenPort string
	BeHost     string
}

func hello(w http.ResponseWriter, r *http.Request) {

	myResp := GetResp{}
	myResp.ResponseAt = time.Now().Local()
	myResp.BeHost, _ = os.Hostname()
	myResp.ListenPort = listenPort

	cnt, ok := r.URL.Query()["count"]
	if !ok || len(cnt) < 1 {
		fmt.Println("Url Param 'count' is missing")
		return
	}
	//else {
	//fmt.Println("Url Param 'count' is ", cnt[0])
	//}
	myResp.ReqCnt, _ = strconv.Atoi(cnt[0])

	sourceIP := r.RemoteAddr
	myResp.SrcIP, _, _ = net.SplitHostPort(sourceIP)

	myRespJSON, err := json.Marshal(myResp)
	if err != nil {
		panic("json marshal err")
	}
	w.Header().Set("Content-Type", "applicaiton/json")
	w.WriteHeader(http.StatusOK)
	w.Write(myRespJSON)
	fmt.Printf("server sent: %v\n", myRespJSON)
}

var mux map[string]func(http.ResponseWriter, *http.Request)

func getMyIP() string {

	addrs, err := net.InterfaceAddrs()
	if err != nil {
		os.Stderr.WriteString("Oops: " + err.Error() + "\n")
		os.Exit(1)
	}

	for _, a := range addrs {
		if ipnet, ok := a.(*net.IPNet); ok && !ipnet.IP.IsLoopback() {
			if ipnet.IP.To4() != nil {
				myIP := ipnet.IP.String()
				return myIP
			}
		}
	}
	return "IP not found"

}

const listenPort string = ":443"

func main() {

	if os.Geteuid() != 0 {
		fmt.Println("you must run with 'sudo'")
		panic("must be sudo")
	}
	// log hostname for this backend
	h, _ := os.Hostname()
	fmt.Println("BE hostname ", h)
	server := http.Server{
		Addr:    listenPort,
		Handler: &myHandler{},
	}
	fmt.Println("hello server listening on:", server.Addr)

	mux = make(map[string]func(http.ResponseWriter, *http.Request))
	mux["/"] = hello

	server.ListenAndServeTLS("server.crt", "server.key")
}

type myHandler struct{}

func (*myHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {

	if h, ok := mux[r.URL.Path]; ok {
		h(w, r)
		return
	} else {
		fmt.Println("mux error on server ")
	}

	fmt.Println("unexpected end of handler ")
}
