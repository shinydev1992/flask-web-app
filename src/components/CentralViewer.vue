<template>
  <div class="central-viewer">
    <h3>Prikaz dokumenta za: {{ currentAgendaItemName }}</h3>
    <iframe v-if="pdfPath" :src="pdfPath" type="application/pdf" width="100%" height="600px"></iframe>
    <p v-else>Nema dostupnog PDF-a za ovu točku.</p>
  </div>
</template>

<script>
export default {
  name: 'CentralViewer',
  data() {
    return {
      currentAgendaItemName: '',
      pdfPath: ''
    };
  },
  props: {
    agendaItemId: {
      type: Number,
      required: true
    }
  },
  watch: {
    agendaItemId: {
      immediate: true,
      handler() {
        this.fetchAgendaItemDetails();
      }
    }
  },
  methods: {
    async fetchAgendaItemDetails() {
      try {
        const response = await fetch(`/agendas/${this.agendaItemId}`); // Pretpostavljam da imate endpoint koji vraća detalje točke dnevnog reda.
        const data = await response.json();
        this.currentAgendaItemName = data.name;
        this.pdfPath = data.pdf_path;
      } catch (error) {
        console.error("Došlo je do pogreške prilikom dohvaćanja detalja točke dnevnog reda:", error);
      }
    }
  }
}
</script>

<style scoped>
.central-viewer {
  flex: 1;
  padding: 10px;
}
</style>
