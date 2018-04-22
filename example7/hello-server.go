package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
)

func hello(w http.ResponseWriter, r *http.Request) {
	//LocalAddrContextKey := &contextKey{"local-addr"}
	myHost, _ := os.Hostname()
	httpMethodStr := r.Method
	sourceIP := r.RemoteAddr
	helloMsg1 := "hello from host: " + myHost + "  HTTP: " + httpMethodStr + "   client source IP: " + sourceIP + "\n"
	helloMsg2 := "hello from host: " + myHost + "  HTTP: " + httpMethodStr + "\n"
	fmt.Println(helloMsg1)
	io.WriteString(w, helloMsg2)
}

var mux map[string]func(http.ResponseWriter, *http.Request)

func main() {
	server := http.Server{
		Addr:    ":82",
		Handler: &myHandler{},
	}

	mux = make(map[string]func(http.ResponseWriter, *http.Request))
	mux["/"] = hello

	server.ListenAndServe()
}

type myHandler struct{}

func (*myHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	if h, ok := mux[r.URL.String()]; ok {
		h(w, r)
		return
	}

	io.WriteString(w, "My server: "+r.URL.String())
}
