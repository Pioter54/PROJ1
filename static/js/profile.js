    const zoneData = {
      'us-west1': ['us-west1-a', 'us-west1-b', 'us-west1-c'],
      'us-west2': ['us-west2-a', 'us-west2-b', 'us-west2-c'],
      'us-west3': ['us-west3-a', 'us-west3-b', 'us-west3-c'],
      'us-west4': ['us-west4-a', 'us-west4-b', 'us-west4-c'],
      'asia-south1': ['asia-south1-a', 'asia-south1-b', 'asia-south1-c'],
      'asia-south2': ['asia-south2-a', 'asia-south2-b', 'asia-south2-c'],
      'asia-east1': ['asia-east1-a', 'asia-east1-b', 'asia-east1-c'],
      'asia-east2': ['asia-east2-a', 'asia-east2-b', 'asia-east2-c'],
      'asia-northeast1': ['asia-northeast1-a', 'asia-northeast1-b', 'asia-northeast1-c'],
      'asia-northeast2': ['asia-northeast2-a', 'asia-northeast2-b', 'asia-northeast2-c'],
      'asia-northeast3': ['asia-northeast3-a', 'asia-northeast3-b', 'asia-northeast3-c'],
      'asia-southeast1': ['asia-southeast1-a', 'asia-southeast1-b', 'asia-southeast1-c'],
      'australia-southeast1': ['australia-southeast1-a', 'australia-southeast1-b', 'australia-southeast1-c'],
      'australia-southeast2': ['australia-southeast2-a', 'australia-southeast2-b', 'australia-southeast2-c'],
      'europe-central2': ['europe-central2-a', 'europe-central2-b', 'europe-central2-c'],
      'europe-north2': ['europe-north2-a', 'europe-north2-b', 'europe-north2-c'],
      'europe-southwest1': ['europe-southwest1-a', 'europe-southwest1-b', 'europe-southwest1-c'],
      'europe-west1': ['europe-west1-b', 'europe-west1-c', 'europe-west1-d'],
      'europe-west2': ['europe-west2-a', 'europe-west2-b', 'europe-west2-c'],
      'europe-west3': ['europe-west3-a', 'europe-west3-b', 'europe-west3-c'],
      'europe-west4': ['europe-west4-a', 'europe-west4-b', 'europe-west4-c'],
      'europe-west6': ['europe-west6-a', 'europe-west6-b', 'europe-west6-c'],
      'europe-west8': ['europe-west8-a', 'europe-west8-b', 'europe-west8-c'],
      'europe-west9': ['europe-west9-a', 'europe-west9-b', 'europe-west9-c'],
      'northamerica-northeast1': ['northamerica-northeast1-a', 'northamerica-northeast1-b', 'northamerica-northeast1-c'],
      'northamerica-northeast2': ['northamerica-northeast2-a', 'northamerica-northeast2-b', 'northamerica-northeast2-c'],
      'southamerica-east1': ['southamerica-east1-a', 'southamerica-east1-b', 'southamerica-east1-c'],
      'us-central1': ['us-central1-a', 'us-central1-b', 'us-central1-c', 'us-central1-f'],
      'us-east1': ['us-east1-b', 'us-east1-c', 'us-east1-d'],
      'us-east4': ['us-east4-a', 'us-east4-b', 'us-east4-c']
    };

    // Machine family configuration
    const machineFamilyData = {
      'us-west1': ['E2', 'N2', 'N2D', 'T2D', 'N1', 'M1', 'C2', 'A2'],
      'us-west2': ['E2', 'N2', 'N2D', 'N1', 'M1', 'C2'],
      'us-west3': ['E2', 'N1', 'N2', 'C2'],
      'us-west4': ['E2', 'N2', 'N2D', 'N1', 'C2', 'T2D', 'M1', 'M2'],
      'asia-south1': ['E2', 'N2', 'N2D', 'N1', 'M1', 'M2', 'C2'],
      'asia-south2': ['E2', 'N1', 'N2', 'M1', 'M2', 'C2'],
      'asia-east1': ['E2', 'N2', 'N2D', 'T2D', 'N1', 'M1', 'C2', 'C2D'],
      'asia-east2': ['E2', 'N2', 'N2D', 'N1', 'C2'],
      'asia-northeast1': ['E2', 'N2', 'N2D', 'N1', 'M1', 'M2', 'C2', 'A2'],
      'asia-northeast2': ['E2', 'N1', 'N2', 'N2D', 'M1', 'M2', 'C2'],
      'asia-northeast3': ['E2', 'N2', 'N1', 'M1', 'C2'],
      'asia-southeast1': ['E2', 'N2', 'N2D', 'T2D', 'N1', 'M1', 'C2', 'C2D', 'A2'],
      'australia-southeast1': ['E2', 'N2', 'N2D', 'T2D', 'N1', 'C2', 'M1', 'M2'],
      'australia-southeast2': ['E2', 'N1', 'N2', 'M1'],
      'europe-central2': ['E2', 'N1', 'N2'],
      'europe-north2': ['E2', 'N2', 'N2D', 'N1', 'C2'],
      'europe-southwest1': ['E2', 'N2'],
      'europe-west1': ['E2', 'N2', 'N2D', 'T2D', 'N1', 'M1', 'M2', 'C2'],
      'europe-west2': ['E2', 'N2', 'N2D', 'T2D', 'N1', 'M1', 'M2', 'C2'],
      'europe-west3': ['E2', 'N2', 'N2D', 'T2D', 'N1', 'M1', 'M2', 'C2'],
      'europe-west4': ['E2', 'N2', 'N2D', 'T2D', 'N1', 'M1', 'M2', 'C2', 'C2D', 'A2'],
      'europe-west6': ['E2', 'N2', 'N1', 'M1', 'C2'],
      'europe-west8': ['E2', 'N2', 'N2D'],
      'europe-west9': ['E2', 'N2'],
      'northamerica-northeast1': ['E2', 'N2', 'N2D', 'N1', 'M1', 'M2', 'C2'],
      'northamerica-northeast2': ['E2', 'N2', 'N1', 'M1'],
      'southamerica-east1': ['E2', 'N2', 'N2D', 'T2D', 'N1', 'M1', 'C2'],
      'us-central1': ['E2', 'N2', 'N2D', 'T2D', 'N1', 'M1', 'M2', 'C2', 'C2D', 'A2'],
      'us-east1': ['E2', 'N2', 'N2D', 'T2D', 'N1', 'M1', 'M2', 'C2', 'C2D'],
      'us-east4': ['E2', 'N2', 'N2D', 'T2D', 'N1', 'M1', 'M2', 'C2', 'C2D']
    };

    const machineFamilyTypes = {
      'E2': ['standard', 'highmem', 'highcpu', 'micro', 'small', 'medium'],
      'N2': ['standard', 'highmem', 'highcpu'],
      'N2D': ['standard', 'highmem'],
      'T2D': ['standard'],
      'N1': ['standard', 'highmem', 'highcpu'],
      'M1': ['ultramem'],
      'M2': ['ultramem'],
      'C2': ['standard', 'highcpu'],
      'C2D': ['standard', 'highcpu'],
      'A2': ['highgpu'],
      'CUSTOM': ['standard', 'highmem', 'highcpu', 'ultramem', 'micro', 'small', 'medium', 'highgpu']
    };

    // Machine vCPU options
    const machineVcpuOptions = {
      'standard': ['2', '4', '8', '16', '32', '64', '96', '128'],
      'highmem': ['2', '4', '8', '16', '32', '64', '96', '128'],
      'highcpu': ['2', '4', '8', '16', '32', '64', '96'],
      'ultramem': ['40', '80', '208', '416'],
      'micro': [''],
      'small': [''],
      'medium': [''],
      'highgpu': ['12', '24', '48', '96'],
      'custom': ['2', '4', '8', '16', '32', '64', '96', '128']
    };

 document.addEventListener("DOMContentLoaded", () => {
    const zoneSelect = document.getElementById('modal_zone');
    const locationSelect = document.getElementById('modal_location');
    const family = document.getElementById("machine_family");
    const type = document.getElementById("machine_family_type");
    const vcpu = document.getElementById("machine_vcpu");
    const full = document.getElementById("machine_type");
    const form = document.querySelector('#createProjectModal form');

    if (!locationSelect || !zoneSelect || !family || !type || !vcpu || !full || !form) return;

    locationSelect.addEventListener('change', function (e) {
      const region = e.target.value;

      // Ustawienia dla stref
      zoneSelect.innerHTML = '';
      if (!region || !zoneData[region]) {
        zoneSelect.setAttribute('disabled', 'disabled');
        zoneSelect.innerHTML = '<option value="" disabled selected>Najpierw wybierz lokalizację</option>';
      } else {
        zoneData[region].forEach(zone => {
          const option = document.createElement('option');
          option.value = zone;
          option.textContent = zone;
          zoneSelect.appendChild(option);
        });
        zoneSelect.removeAttribute('disabled');
      }

      // Reset i załadowanie rodzin maszyn
      family.innerHTML = '<option value="" disabled selected>Rodzina</option>';
      type.innerHTML = '<option value="" disabled selected>Typ</option>';
      vcpu.innerHTML = '<option value="" disabled selected>vCPU</option>';
      family.disabled = true;
      type.disabled = true;
      vcpu.disabled = true;

      if (!machineFamilyData[region]) return;

      machineFamilyData[region].forEach(f => {
        const option = document.createElement('option');
        option.value = f.toLowerCase();
        option.textContent = f;
        family.appendChild(option);
      });
      family.disabled = false;
    });

    family.addEventListener("change", () => {
      const selectedFamily = family.value.toUpperCase();
      type.innerHTML = '<option value="" disabled selected>Typ</option>';
      vcpu.innerHTML = '<option value="" disabled selected>vCPU</option>';
      type.disabled = true;
      vcpu.disabled = true;

      if (!machineFamilyTypes[selectedFamily]) return;

      machineFamilyTypes[selectedFamily].forEach(t => {
        const option = document.createElement('option');
        option.value = t;
        option.textContent = t;
        type.appendChild(option);
      });
      type.disabled = false;
    });

    type.addEventListener("change", updateMachineType);
    vcpu.addEventListener("change", updateMachineType);
    form.addEventListener("submit", () => updateMachineType());

    function updateMachineType() {
      const familyVal = family.value;
      const typeVal = type.value;
      const vcpuVal = vcpu.value;
      const disabledTypes = ["micro", "small", "medium"];

      if (disabledTypes.includes(typeVal)) {
        vcpu.innerHTML = '';
        const option = document.createElement('option');
        option.value = '';
        option.textContent = 'Brak dostępnych opcji';
        option.selected = true;
        vcpu.appendChild(option);
        vcpu.disabled = true;
        full.value = `${familyVal}-${typeVal}`;
      } else {
        vcpu.disabled = false;
        vcpu.innerHTML = `
          <option value="" disabled selected>vCPU</option>
          <option value="2">2</option>
          <option value="4">4</option>
          <option value="8">8</option>
          <option value="16">16</option>
          <option value="32">32</option>
          <option value="64">64</option>
          <option value="96">96</option>
          <option value="128">128</option>
        `;
        if (familyVal && typeVal && vcpuVal) {
          full.value = `${familyVal}-${typeVal}-${vcpuVal}`;
        } else {
          full.value = "";
        }
      }
    }

    document.getElementById('createProjectModal')?.addEventListener('hidden.bs.modal', function () {
      this.querySelector('form').reset();
      zoneSelect.innerHTML = '<option value="" disabled selected>Najpierw wybierz lokalizację</option>';
      zoneSelect.setAttribute('disabled', 'disabled');
      family.innerHTML = '<option value="" disabled selected>Rodzina</option>';
      family.setAttribute('disabled', 'disabled');
      type.innerHTML = '<option value="" disabled selected>Typ</option>';
      type.setAttribute('disabled', 'disabled');
      vcpu.innerHTML = '<option value="" disabled selected>vCPU</option>';
      vcpu.setAttribute('disabled', 'disabled');
      full.value = "";
    });
  });

  document.addEventListener('DOMContentLoaded', function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl)
    })
});

document.addEventListener("DOMContentLoaded", () => {
  const gcpContainer = document.getElementById('gcp-resources');
  if (!gcpContainer) return;

  gcpContainer.innerHTML = ""; // usuwa "Ładowanie danych..."

  if (window.vmInstances && Array.isArray(window.vmInstances)) {
    const vmBlock = document.createElement('div');
    vmBlock.innerHTML = '<h4>Instancje VM</h4>' +
      (window.vmInstances.length === 0
        ? '<p class="text-muted">Brak uruchomionych maszyn.</p>'
        : '<ul class="list-group mb-3">' +
          window.vmInstances.map(vm => `<li class="list-group-item d-flex justify-content-between align-items-center">
            <span><strong>${vm.name}</strong> (${vm.zone})</span>
            <span class="badge bg-${vm.status === 'RUNNING' ? 'success' : 'secondary'}">${vm.status}</span>
          </li>`).join('') +
          '</ul>');
    gcpContainer.appendChild(vmBlock);
  }

  if (window.gcsBuckets && Array.isArray(window.gcsBuckets)) {
    const bucketBlock = document.createElement('div');
    bucketBlock.innerHTML = '<h4>Bucket\'y Storage</h4>' +
      (window.gcsBuckets.length === 0
        ? '<p class="text-muted">Brak bucketów w projekcie.</p>'
        : '<ul class="list-group">' +
          window.gcsBuckets.map(name => `<li class="list-group-item">${name}</li>`).join('') +
          '</ul>');
    gcpContainer.appendChild(bucketBlock);
  }
});
