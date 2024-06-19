export async function getUserDataFromAuthAPI(){
  try{
    const token = localStorage["userState"]
    const headers = {
        "Authorization": `Bearer ${token}`
      }
    const response = await fetch("/api/user/auth",{
      method:"GET",
      headers: headers
    })
    const responseJSON = await response.json()
    const data = responseJSON["data"]
    return data
  }catch{
    console.log("fetch fail api/user/auth")
  }
}