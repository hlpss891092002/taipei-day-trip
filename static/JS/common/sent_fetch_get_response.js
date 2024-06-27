export async function sentFetchWithBody(method , body){
  const token = localStorage["userState"] ? localStorage["userState"] : ""
  const headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": `Bearer ${token}`
      }
      let response = await fetch("/api/booking",{
        method:`${method.toUpperCase()}`,
        headers: headers,
        body: JSON.stringify(body)
      })
      let data = response.json()
      return data
}
export async function sentFetchWithoutBody(method){
  const token = localStorage["userState"] ? localStorage["userState"] : ""
  const headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": `Bearer ${token}`
      }
      let response = await fetch("/api/booking",{
        method:`${method.toUpperCase()}`,
        headers: headers,
      })
      let data = response.json()
      return data
}