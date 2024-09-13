import { supabase } from './supabase'
import { createDefaultState } from './consts'

export default createDefaultState(async () => {
  return await supabase
    .from('games')
    .select(`*`)
})
