package main

import (
  "wiimote"
  "fmt"
	"github.com/davecheney/gpio"
	"github.com/davecheney/gpio/rpi"
  "time"
)

func main() {
	fmt.Printf("Scanning for wiimote, press buttons 1 and 2 now...\n")
	scanPin, err := gpio.OpenPin(rpi.GPIO25, gpio.ModeOutput)
	if err != nil {
		fmt.Printf("Error opening pin! %s\n", err)
		return
	}

	connectedPin, err := gpio.OpenPin(rpi.GPIO24, gpio.ModeOutput)
	if err != nil {
		fmt.Printf("Error opening pin! %s\n", err)
		return
	}
  scanPin.Set()
  wm := wiimote.Scan()
  scanPin.Clear()
	connectedPin.Set()
  fmt.Printf("Connected, perhaps.\n")
  for {
    fmt.Printf("Button 1: %t.\n", wm.Button1Pressed())
    time.Sleep(2 * 1000 * time.Millisecond)
  }
}
