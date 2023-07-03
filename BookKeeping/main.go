package main

import (
	"fmt"
	wb "workbook/workbook"
	gp "graphics/graphics"
)

func main() {
	f := wb.Get_file()
	defer func() {
		if err := f.Close(); err != nil {
			fmt.Println(err)
		}
	}()

}
