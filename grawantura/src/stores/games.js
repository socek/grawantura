import { supabase, createDefaultState } from './supabase'

export default createDefaultState("games", async () => {
  return await supabase
    .from('games')
    .select(`*`)
})
