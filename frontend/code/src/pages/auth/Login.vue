<template>
  <VaForm ref="form" @submit.prevent="submit">
    <h1 class="font-semibold text-4xl mb-4">Log in</h1>
    <p class="text-base mb-4 leading-5">
      New to Vuestic?
      <RouterLink :to="{ name: 'signup' }" class="font-semibold text-primary">Sign up</RouterLink>
    </p>
    <VaInput
      v-model="formData.email"
      :rules="[validators.required, validators.email]"
      class="mb-4"
      label="Email"
      type="email"
    />
    <VaValue v-slot="isPasswordVisible" :default-value="false">
      <VaInput
        v-model="formData.password"
        :rules="[validators.required]"
        :type="isPasswordVisible.value ? 'text' : 'password'"
        class="mb-4"
        label="Password"
        @clickAppendInner.stop="isPasswordVisible.value = !isPasswordVisible.value"
      >
        <template #appendInner>
          <VaIcon
            :name="isPasswordVisible.value ? 'mso-visibility_off' : 'mso-visibility'"
            class="cursor-pointer"
            color="secondary"
          />
        </template>
      </VaInput>
    </VaValue>

    <div class="flex justify-center mt-4">
      <VaButton class="w-full" @click="submit"> Login</VaButton>
    </div>
  </VaForm>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useForm, useToast } from 'vuestic-ui'
import { validators } from '../../services/utils'
import { supabase } from '@/stores/supabase'

const { validate } = useForm('form')
const { push } = useRouter()
const { init } = useToast()

const formData = reactive({
  email: '',
  password: '',
})

const handleLogin = async () => {
  try {
    const { error } = await supabase.auth.signInWithPassword({
      email: formData.email,
      password: formData.password,
    })
    if (error) throw error
    push({ name: 'dashboard' })
  } catch (error) {
    if (error instanceof Error) {
      init({"message": error.message, color: "#FF0000"})
    }
  }
}

const submit = async () => {
  if (validate()) {
    handleLogin()
  }
}
</script>
