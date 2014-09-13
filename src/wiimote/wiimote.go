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

func Scan() {
	//C.cwiid_set_err(C.wiierr)
	addr := C.any()
	fmt.Printf("Scanning for wiimote, press buttons 1 and 2 now...\n")
	_, err := C.cwiid_open(addr, 0)
	if err != nil {
		fmt.Printf("error reported?\n")
	}
	time.Sleep(10 * 1000 * time.Millisecond)
	fmt.Printf("Wiimote found but I'm exiting anyway.\n")
}
