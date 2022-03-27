<template>
  <elFrame :src="ManagementApi" />
</template>
<script>
import elFrame from './components/iframe'
export default {
  name: 'Swagger',
  components: { elFrame },
  data() {
    return {
      ManagementApi: process.env.VUE_APP_BASE_API + '/oauth/register/'
    }
  }
}
</script>
