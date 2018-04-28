package main

// http-clinet.go - program to send http GET to server and collect responses
//
// command: http-client serverIp serverPort numItterations
//
// Name: R. Melton
// Date:  4/23/18
import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"
	"time"
)

func usage() {
	fmt.Println("usage http-client serverIp serverPort numItterations")
	panic("parameter error")
}

// GetResp json response structure
type GetResp struct {
	ResponseAt time.Time
	ReqCnt     int
	SrcIP      string
	ListenPort string
	BeHost     string
}

func main() {

	type hostMessage struct {
		Host  string
		srcIp string
	}
	if len(os.Args) != 4 {
		usage()
	}
	targetIP := os.Args[1]
	targetPort := os.Args[2]
	numItterations, _ := strconv.Atoi(os.Args[3])

	client := &http.Client{}

	url := "http://" + targetIP + ":" + targetPort
	i := 0
	responseMap := make(map[string]int)

	// build requests, send them to the server, read responses
	for i = 0; i < numItterations; i++ {
		req, err := http.NewRequest("GET", url, nil)
		if err != nil {
			log.Print(err)
			os.Exit(1)
		}

		q := req.URL.Query()
		iStr := strconv.Itoa(i)
		// count is the incrementing number that goes with each request
		q.Add("count", iStr)
		req.URL.RawQuery = q.Encode()

		//fmt.Println("req URL string is ", req.URL.String())
		resp, err := client.Do(req)
		if err != nil {
			fmt.Println("resp error", err)
			os.Exit(1)
		} else {
			jsonResp := GetResp{}
			json.NewDecoder(resp.Body).Decode(&jsonResp)
			if jsonResp.ReqCnt != i {
				fmt.Println("response out of order error ", jsonResp.ReqCnt, i)
			}
			//fmt.Println(" resp json ", jsonResp.BeHost, jsonResp.ListenPort, jsonResp.ReqCnt, jsonResp.ResponseAt, jsonResp.SrcIP)
			responseMap[jsonResp.BeHost]++
		}

		defer resp.Body.Close()

	}

	// show results from each LB backend host
	fmt.Println("\ntotal requests sent to server ", numItterations)
	fmt.Println("\ntotal number server backends ", len(responseMap))
	fmt.Println("\nhost\t\t\tpercent total")
	for host, returnCnt := range responseMap {
		num := float64(returnCnt)
		percent := (num / float64(numItterations)) * 100
		fmt.Println(host, "\t\t", percent)
	}

}
