class Api {
    constructor(apiUrl) {
        this.apiUrl = apiUrl;
    }

    getPurchases() {
        return fetch(`/purchases`, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(e => {
                if (e.ok) {
                    return e.json()
                }
                return Promise.reject(e.statusText)
            })
    }

    addPurchases(id) {
        return fetch(`/purchases`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', 'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                id: id
            })
        })
            .then(e => {
                if (e.ok) {
                    return e.json()
                }
                return Promise.reject(e.statusText)
            })
    }

    removePurchases(id) {
        return fetch(`/purchases/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json', 'X-CSRFToken': csrftoken
            }
        })
            .then(e => {
                if (e.ok) {
                    return e.json()
                }
                return Promise.reject(e.statusText)
            })
    }

    addSubscriptions(id) {
        return fetch(`/subscriptions/${id}/follow/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', 'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                id: id
            })
        })
            .then(e => {
                if (e.ok) {
                    return e.json()
                }
                return Promise.reject(e.statusText)
            })
    }

    removeSubscriptions(id) {
        return fetch(`/subscriptions/${id}/unfollow/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json', 'X-CSRFToken': csrftoken
            }
        })
            .then(e => {
                if (e.ok) {
                    return e.json()
                }
                return Promise.reject(e.statusText)
            })
    }

    addFavorites(id) {
        return fetch(`/favorites`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', 'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                id: id
            })
        })
            .then(e => {
                if (e.ok) {
                    return e.json()
                }
                return Promise.reject(e.statusText)
            })
    }

    removeFavorites(id) {
        return fetch(`/favorites/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json', 'X-CSRFToken': csrftoken
            }
        })
            .then(e => {
                if (e.ok) {
                    return e.json()
                }
                return Promise.reject(e.statusText)
            })
    }

    getIngredients(text) {
        return fetch(`/recipes/create-recipe/ingredients?query=${text}`, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(e => {
                if (e.ok) {
                    return e.json()
                }
                return Promise.reject(e.statusText)
            })
    }
}
