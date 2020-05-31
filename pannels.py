def shortNotExists(self):
    self.wfile.write(bytes("""
    <script>
        function directToHomepage() {
            window.location = "http://127.0.0.1/";
        }
    </script>


    <title>Short URL not found</title>
    <h1>Error: Could not find the redirect path for the URL provided</h1>
    <p>That URL does not exist in our databace, make sure you typed in the URL correctly and try again</p>
    <span style="padding-left:100px"></span><button onClick="directToHomepage()">Click Here to Claim this URL</button>
    ""","utf-8"))

def createShortUrl(self):
    self.wfile.write(bytes("""
    <script>
        var xhttp = new XMLHttpRequest();

        function sendUrl() {
            url = document.getElementById("shortUrlBox").value;

            xhttp.onreadystatechange = function() {
                var box = document.getElementById("shortUrlBox")
                box.value = this.responseText;
                box.select()
            }

            xhttp.open("POST", "shortUrl", true);
            xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhttp.send("ShortUrl:" + url);
        }
    </script>

    <title>Url Shortener</title>
    <h1>Create a Short Url</h1>
    <p>Enter the url you want to shorten, then press Get URL</p>
    <span>Enter Url: </span><input type="text" id="shortUrlBox"></input><button id="getUrlBtn" onClick="sendUrl()">Get Url</button>
    ""","utf-8"))