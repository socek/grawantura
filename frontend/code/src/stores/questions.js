import { supabase, createDefaultState } from './supabase'

export default createDefaultState("questions", async () => {
  return await supabase
    .from('questions')
    .select(`*`)
})
