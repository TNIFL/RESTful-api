const searchParams = new URLSearchParams(location.search);

for (const param of searchParams) {
    console.log(param);
}