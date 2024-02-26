package main 
  
// Importing packages 
import ( 
    "fmt"
	"net/http"
	"sync"
	"io"
) 
  
func print_http(url string) { 
  
	resp, err := http.Get(url)
	if err != nil{
		fmt.Println(err)
	}
	defer resp.Body.Close()
	b, err := io.ReadAll(resp.Body)
	if err != nil{
		fmt.Println(err)
	}
	fmt.Println(string(b))
  
} 
// Main function 
func main() { 
	var wg sync.WaitGroup
	print_http("https://api.sampleapis.com/beers/ale")
	wg.Add(1)
	wg.Wait()
} 