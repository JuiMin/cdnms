export const post = (url, params, body, onSuccess, onFailure) => {
    if (params && isObject(params)) {
        Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
    }
    return fetch(url, { method: 'post', body: JSON.stringify(body) })
        .then(response => {
            if (!response.ok) {
                throw Error(response.statusText);
            }
            return response;
        })
        .then(response => {
            if (onSuccess && isFunction(onSuccess)) {
                onSuccess(response);
            }
        }, (error) => {
            if (onFailure && isFunction(onFailure)) {
                onFailure(error)
            }
        });
}

export const get = (url, params, onSuccess, onFailure) => {
    if (params && isObject(params)) {
        Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
    }
    return fetch(url, { method: 'get' })
        .then(response => {
            if (!response.ok) {
                throw Error(response.statusText);
            }
            return response;
        })
        .then(response => {
            if (onSuccess && isFunction(onSuccess)) {
                onSuccess(response);
            }
        }, (error) => {
            if (onFailure && isFunction(onFailure)) {
                onFailure(error)
            }
        });
}

function isFunction(functionToCheck) {
    return functionToCheck && {}.toString.call(functionToCheck) === '[object Function]';
}

function isObject(objectToCheck) {
    return !isFunction(objectToCheck) && typeof objectToCheck === 'object' && objectToCheck !== null;
}