import axios from 'axios'
import { DEFAULT_UNAUTHORIZE_ROUTE } from "@/base/consts"
import useAuthStore from "@/auth/store"
import Router from "@/router"

export default async (request) => {
  const authStore = useAuthStore()
  request["headers"] = request["headers"] || {}
  request["headers"]["auth_token"] = authStore.getToken
  try {
    return await axios(request)
  } catch (error) {
    if(error.status == 401){
      authStore.clearToken()
      Router.push(DEFAULT_UNAUTHORIZE_ROUTE)
    }
    throw error
  }
}
