const like = document.getElementById('like')
const postId = like.getAttribute('data-postid');
// const csrf = document.getElementsByName('csrfmiddlewaretoken')

// https://docs.djangoproject.com/en/4.0/ref/csrf/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// いいね機能
const likePost = () => {
    const csrftoken = getCookie('csrftoken'); 
    const res = fetch(`like/${postId}`,
        {
            method: 'POST', 
            body: JSON.stringify({}),
            credentials: "same-origin",
            headers: { 
                // "X-CSRFToken": csrf[0].value,
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/json; charset=utf-8" 
            }
        }
    )
    .then(res => {
        return res.json();
    })
    .then(result => {
        // htmlを変更
        if(result.data==='like'){
            like.classList.remove('bx-heart')
            like.classList.add('bxs-heart')
        }else if(result.data==='unlike'){
            like.classList.remove('bxs-heart')
            like.classList.add('bx-heart')
        }
    })
    .catch((e) =>{
        console.log(e)
    });

}

like.addEventListener('click', e=>{
    likePost();
})

