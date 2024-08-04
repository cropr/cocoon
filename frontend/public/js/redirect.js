const l = window.location
console.log("checking hostname", l.hostname)
if (l.hostname == "cocoon.be") {
  console.log("redirecting")
  location.replace(`${l.protocol}//www.cocoon.be${l.pathname}${l.search}`)
}
