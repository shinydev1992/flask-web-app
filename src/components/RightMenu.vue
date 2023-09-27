<template>
  <div class="right-menu">
    <div v-for="party in parties" :key="party.party_id" class="party-section">
      <h4>{{ party.party_name }}</h4>
      <ul>
        <li v-for="user in party.members" :key="user.user_id" class="council-member">
          <span :class="['vote-status', user.vote_decision]"></span>
          {{ user.name }} {{ user.last_name }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RightMenu',
  data() {
    return {
      parties: []
    };
  },
  created() {
    this.fetchPartiesAndMembers();
  },
  methods: {
    async fetchPartiesAndMembers() {
      try {
        const response = await fetch('/parties-with-members'); // Pretpostavljam da imate endpoint koji vraća sve stranke s članovima.
        this.parties = await response.json();
      } catch (error) {
        console.error("Došlo je do pogreške prilikom dohvaćanja stranaka i članova:", error);
      }
    }
  }
}
</script>

<style scoped>
.right-menu {
  padding: 10px;
}

.party-section {
  margin-bottom: 20px;
}

.council-member {
  display: flex;
  align-items: center;
}

.vote-status {
  display: inline-block;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-right: 10px;
}

.vote-status.FOR {
  background-color: green;
}

.vote-status.AGAINST {
  background-color: red;
}

.vote-status.ABSTAIN {
  background-color: yellow;
}
</style>
