# GAloopedrequest
Sample code for looping through google analytics client view ID's, and circumventing the 10 request a second limit.

when using google analytics, most websites help you set up the correct API key and permissions. under an account you can have multiple clients with unique accounts, then webID's and viewID's. It is easy to individually pull down certain metrics, but becomes more difficult when looping through multiple accounts, as the GA API only allows 10 requests a second, and 100 requests per 100 seconds. Using exponential backoff this can be circumvented. 
