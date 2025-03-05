package main

import (
	"log"
	"aks-upgrade-cli/cmd"
)

func main() {
	if err := cmd.Execute(); err != nil { 
		log.Fatal(err)
	}
}
