import axios from 'axios';
import useAuthStore from './store'

import {AUTH_URL} from "./consts"

const authStore = useAuthStore()

export const authorize = async (email, password) => {
  let result = null
  try {
    result = await axios.post(AUTH_URL,
      {
        email: email,
        password: password,
     }
    )
  } catch (error) {
    console.log(error)
    return false
  }
  if(result.data["status"] == "success") {
    authStore.setToken(result.data["token"])
  } else {
    return false;
  }
  return true
}
