
function selectCurrentStatus(status) {
  var select = document.getElementById('status-query');
  for (i = 0; i < select.options.length; i++) {
    if (select.options[i].value == status) {
      select.selectedIndex = i
      break
    }
  }
}

function selectCurrentWorkflow(workflow_id) {
  var select = document.getElementById('workflow-query');
  for (i = 0; i < select.options.length; i++) {
    if (select.options[i].value == workflow_id) {
      select.selectedIndex = i
      break
    }
  }

}

selectCurrentWorkflow(currentWorkflowId)
selectCurrentStatus(status)
