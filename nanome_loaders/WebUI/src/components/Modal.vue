<template>
  <div v-if="showing" @click.self="cancel" class="modal">
    <div class="modal-body">
      <div class="p-4">
        <h2 v-if="options.title">{{ options.title }}</h2>
        <p v-if="options.body" v-html="options.body"></p>

        <div class="mt-2">
          <template v-if="options.type === 'prompt'">
            <input ref="prompt" v-model="input1" type="text" />
          </template>

          <template v-else-if="options.type === 'login'">
            <input
              ref="login"
              v-model="input1"
              :class="{ 'border-red-500': error }"
              placeholder="username"
              type="text"
            />
            <input
              v-model="input2"
              :class="{ 'border-red-500': error }"
              placeholder="password"
              type="password"
            />

            <p v-if="error" class="text-red-500">
              incorrect login or password
            </p>

            <p>
              <a
                href="https://home.nanome.ai/login/forgot"
                target="_blank"
                class="link text-blue-500"
              >
                forgot password?
              </a>
            </p>
          </template>
        </div>
      </div>

      <div class="modal-actions">
        <button
          v-if="options.type !== 'alert'"
          @click="cancel"
          class="btn"
          :class="options.cancelClass"
        >
          {{ options.cancelTitle }}
        </button>
        <button
          @click="ok"
          class="btn"
          :class="options.okClass"
          :disabled="loading"
        >
          {{ options.okTitle }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
const defaults = {
  type: 'confirm',
  title: '',
  body: '',
  default: '',
  okTitle: 'ok',
  okClass: '',
  cancelTitle: 'cancel',
  cancelClass: 'danger'
}

const deferred = () => {
  let res, rej

  const promise = new Promise((resolve, reject) => {
    res = resolve
    rej = reject
  })

  promise.resolve = res
  promise.reject = rej

  return promise
}

export default {
  data: () => ({
    showing: false,
    error: false,
    loading: false,
    options: {
      type: 'login',
      title: 'title',
      body: 'body',
      default: '',
      okTitle: 'ok',
      okClass: '',
      cancelTitle: 'cancel',
      cancelClass: 'danger'
    },
    input1: '',
    input2: '',
    deferred: deferred()
  }),

  mounted() {
    document.body.addEventListener('keydown', this.onKeydown)
  },

  destroyed() {
    document.body.removeEventListener('keydown', this.onKeydown)
  },

  methods: {
    onKeydown(e) {
      if (!this.showing) return

      if (e.key === 'Enter') {
        this.ok()
      } else if (e.key === 'Escape') {
        this.cancel()
      }
    },

    show(options) {
      Object.assign(this.options, defaults, options)
      this.showing = true

      if (this.options.type === 'prompt') {
        this.input1 = this.options.default
        this.$nextTick(() => {
          const input = this.$refs.prompt
          input.focus()
          input.setSelectionRange(0, input.value.length)
        })
      } else if (this.options.type === 'login') {
        this.$nextTick(() => this.$refs.login.focus())
      }

      this.deferred = deferred()
      return this.deferred
    },

    alert(options) {
      return this.show({
        type: 'alert',
        ...options
      })
    },

    confirm(options) {
      return this.show({
        type: 'confirm',
        ...options
      })
    },

    prompt(options) {
      return this.show({
        type: 'prompt',
        ...options
      })
    },

    login(options) {
      return this.show({
        type: 'login',
        title: 'Log in to Nanome',
        body: 'Log in using your Nanome account',
        okTitle: 'log in',
        okClass: 'primary',
        cancelClass: '',
        ...options
      })
    },

    reset() {
      this.showing = false
      this.input1 = ''
      this.input2 = ''
      this.deferred = null
    },

    cancel() {
      if (this.options.type === 'confirm') {
        this.deferred.resolve(false)
      } else {
        this.deferred.resolve(undefined)
      }

      this.reset()
    },

    ok() {
      let data
      if (this.options.type === 'confirm') {
        data = true
      } else if (this.options.type === 'prompt') {
        data = this.input1
      } else if (this.options.type === 'login') {
        this.attemptLogin()
        return
      }

      this.deferred.resolve(data)
      this.reset()
    },

    async attemptLogin() {
      this.error = false
      this.loading = true

      const creds = {
        username: this.input1,
        password: this.input2
      }

      const success = await this.$store.dispatch('login', creds)
      this.loading = false

      if (success) {
        this.deferred.resolve(true)
        this.reset()
      } else {
        this.error = true
      }
    }
  }
}
</script>

<style lang="scss">
.modal {
  @apply fixed inset-0 z-50 flex items-center justify-center;
  background: rgba(0, 0, 0, 0.5);

  &-body {
    @apply bg-white rounded shadow overflow-hidden;
    width: 20rem;
  }

  &-actions {
    @apply w-full flex justify-between;

    button {
      @apply w-full;
    }
  }
}
</style>
