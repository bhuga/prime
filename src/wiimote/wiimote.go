package wiimote

import "fmt"

//import "unsafe"

/*
#include <stdlib.h>
#include <stdio.h>
#include <bluetooth/bluetooth.h>
#include <cwiid.h>
#cgo LDFLAGS: -lcwiid
void myprint(char* s) {
        printf("printing from c: %s\n", s);
}

void wiierr(cwiid_wiimote_t *wiimote, const char *s, va_list ap)
{
	if (wiimote) printf("%d:", cwiid_get_id(wiimote));
	else printf("-1:");
	vprintf(s, ap);
	printf("\n");
}

bdaddr_t *any() {
  malloc(sizeof(bdaddr_t));
}
*/
import "C"
import "time"

type Wiimote struct {
	cwiid_wiimote C.cwiid_wiimote_t
}


func Scan() {
	//C.cwiid_set_err(C.wiierr)
	addr := C.any()
  var controller *C.cwiid_wiimote_t
  var controller_state C.struct_cwiid_state
	fmt.Printf("Scanning for wiimote, press buttons 1 and 2 now...\n")
	controller, err := C.cwiid_open(addr, 0)
	if err != nil {
		fmt.Printf("error reported?\n")
	}
  if controller == nil {
    fmt.Printf("controller is nil, shucks\n")
  }
  fmt.Printf("Connected, perhaps.\n")
  state := C.uint8_t(0)

  upcoming := 1
  C.cwiid_get_state(controller, &controller_state)
  C.cwiid_set_rpt_mode(controller, controller_state.rpt_mode | C.CWIID_RPT_ACC | C.CWIID_RPT_BTN)
  for {
    if upcoming == 1 {
      state = C.CWIID_LED1_ON
      upcoming = 2
    } else {
      state = C.CWIID_LED2_ON
      upcoming = 1
    }

    fmt.Printf("setting leds %v\n", int(state))
    res, err := C.cwiid_set_led(controller, state)
    if err != nil {
      fmt.Printf("error setting leds\n")
    }
    if res != 0 {
      fmt.Printf("set led had errors\n")
    }

    res, err = C.cwiid_get_state(controller, &controller_state)
    if res != 0 {
      fmt.Printf("Failure to get state: %v\n", res)
    }
    if err != nil {
      fmt.Printf("failed getting state\n")
    }
	  if (controller_state.led & C.CWIID_LED1_ON == C.CWIID_LED1_ON) {
      fmt.Printf("led 1 is on\n")
    }
    fmt.Printf("rpt:%d led:%d rumb:%d bat:%d butt:%d err:%d\n", controller_state.rpt_mode, controller_state.led, controller_state.rumble, controller_state.battery, controller_state.buttons, controller_state.error)
  
    time.Sleep(2 * 1000 * time.Millisecond)
  }
	fmt.Printf("Wiimote found but I'm exiting anyway.\n")
}
