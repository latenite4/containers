package main

// log-maker - program to generate output to stdout which will be log messages
// from a container within a pod.
// name R. Melton
// date: 4/7/18

import (
	"fmt"
	"log/syslog"
	"math/rand"
	"os"
	"time"
)

func main() {
	var writeToLog bool = true
	myVer := "1.0"
	//fmt.Println("log-maker program starting...")
	myhostname, ok := os.Hostname()

	if ok != nil {
		panic("error getting hostname")
	}
	s1 := rand.NewSource(time.Now().UnixNano())
	r1 := rand.New(s1)
	myProgramName := os.Args[0]

	l3, err := syslog.New(syslog.LOG_ERR, "GoExample")
	if err != nil {
		//fmt.Println("error opening syslog")
		writeToLog = false
	}
	// continually generate logs
	for {
		randomNumber := r1.Intn(100)
		//myTime := time.Now()
		myError := "level0"
		if randomNumber < 10 {
			myError = "level1"
		} else if randomNumber < 20 {
			myError = "level2"
		}
		// write to stdout

		//dont add timestamp to log message; it is already provided
		//myTimeString := myTime.Format(time.ANSIC)
		stdoutString := "logto: stdout " + "host: " + myhostname + " program: " + myProgramName + " error_level: " + myError + " app version: " + myVer
		fmt.Println(stdoutString)

		// only write to syslog when no errors; syslog is not used when this program runs inside a container.
		if writeToLog {
			syslogString := "logto: syslog " + "host: " + myhostname + " program: " + myProgramName + " error_level: " + myError + " app version: " + myVer
			l3.Info(syslogString)
		}

		time.Sleep(5 * time.Second) // just sleep for 5 seconds
	}
}
