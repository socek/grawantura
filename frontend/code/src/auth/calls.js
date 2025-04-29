import axios from 'axios'
import colors from '@/base/colors'
import { useToast } from 'vuestic-ui'
import { DEFAULT_UNAUTHORIZE_ROUTE } from "@/base/consts"
import useAuthStore from "@/auth/store"
import Router from "@/router"

const { init: notify } = useToast()

export const jwtCall = async (request) => {
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

export const jwtCallWithErrorHandling = async (options, texts, parseData) => {
  let result;
  try {
    result = await jwtCall(options)
  } catch(error) {
    notify({
      message: texts.failed,
      color: colors.fail,
    })
    throw error
  }
  if(parseData) {
    return parseData(result, notify)
  } else {
    notify({
      message: texts.success,
      color: colors.success,
    })
    return result;
  }
}

export default jwtCall;
