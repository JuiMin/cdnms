export const post = (
  url: string,
  params?: object,
  body?: object,
  onSuccess?: (res: any) => void,
  onFailure?: (err: Error) => void
) => {
  // @ts-ignore
  params &&
    Object.keys(params).forEach((key) =>
      url.searchParams.append(key, params[key])
    );
  return fetch(url, { method: "post", body: JSON.stringify(body) })
    .then((response) => {
      if (!response.ok) {
        throw Error(response.statusText);
      }
      return response;
    })
    .then(
      (response) => {
        onSuccess && onSuccess(response);
      },
      (error) => {
        onFailure && onFailure(error);
      }
    );
};

export const get = (
  url: string,
  params?: object,
  onSuccess?: (res: any) => void,
  onFailure?: (err: Error) => void
) => {
  // @ts-ignore
  params &&
    Object.keys(params).forEach((key) =>
      url.searchParams.append(key, params[key])
    );
  return fetch(url, { method: "get" })
    .then((response) => {
      if (!response.ok) {
        throw Error(response.statusText);
      }
      return response;
    })
    .then(
      (response) => {
        onSuccess && onSuccess(response);
      },
      (error) => {
        onFailure && onFailure(error);
      }
    );
};
