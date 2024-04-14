document.getElementById("copyright").innerHTML = new Date().getFullYear();

//comments
const editButtons = document.getElementsByClassName("btn-edit");
const commentTitleText = document.getElementById("id_title");
const commentText = document.getElementById("id_body");
const commentForm = document.getElementById("commentForm");
const submitButton = document.getElementById("submitButton");

const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
const deleteButtons = document.getElementsByClassName("btn-delete");
const deleteConfirm = document.getElementById("deleteConfirm");

document.addEventListener('DOMContentLoaded', function() {
    /**
    * Initializes edit functionality for the provided edit buttons.
    *
    * For each button in the `editButtons` collection:
    * - Retrieves the associated comment's ID upon click.
    * - Fetches the content of the corresponding comment.
    * - Populates the `commentText` input/textarea with the comment's content for editing.
    * - Updates the submit button's text to "Update".
    * - Sets the form's action attribute to the `edit_comment/{commentId}` endpoint.
    */
    for (let button of editButtons) {
      button.addEventListener("click", (e) => {
        let target_elem = e.target
        if ( e.target.tagName == 'I')
        {
            target_elem = e.target.parentElement
        }
        let commentId = target_elem.getAttribute("comment_id");
        let commentTitle = document.getElementById(`comment-title${commentId}`).innerText;
        let commentContent = document.getElementById(`comment-body${commentId}`).innerText;
        commentTitleText.value = commentTitle;
        commentText.value = commentContent;
        submitButton.innerText = "Update";
        commentForm.setAttribute("action", `edit_comment/${commentId}`);
      });
    }

    /**
    * Initializes deletion functionality for the provided delete buttons.
    *
    * For each button in the `deleteButtons` collection:
    * - Retrieves the associated comment's ID upon click.
    * - Updates the `deleteConfirm` link's href to point to the
    * deletion endpoint for the specific comment.
    * - Displays a confirmation modal (`deleteModal`) to prompt
    * the user for confirmation before deletion.
    */
    for (let button of deleteButtons) {
      button.addEventListener("click", (e) => {
        let target_elem = e.target
        if ( e.target.tagName == 'I')
        {
            target_elem = e.target.parentElement
        }
        let commentId = target_elem.getAttribute("comment_id");
        deleteConfirm.href = `delete_comment/${commentId}`;
        deleteModal.show();
      });
    }
});
