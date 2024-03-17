function deleteActivity(opporId) {
    fetch("/delete_opportunity", {
      method: "POST",
      body: JSON.stringify({ opporId: opporId }),
    }).then((_res) => {
      window.location.href = "/secret_admin";
    });
}

function addActivity(opporId) {
  fetch("/register_opportunity", {
    method: "POST",
    body: JSON.stringify({ opporId: opporId }),
  }).then((_res) => {
    window.location.href = "/home";
  });
}