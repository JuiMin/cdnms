// NB: All Routes are relative to the domain

// createRoom takes a room name and submits a request to create a room
function createRoom(name) {
    console.log("Attempting to create room for " + name);
    $.post(
        "/",
        {
            name: name,
        },
        function (data, status) {
            if (status == "success") {
                // On success route to the new room
                window.location.href = "room/" + data.room_id;
            } else if (data.error_message) {
                // Check if we sent back an error message of some kind
                alert(data.error_message);
            } else {
                console.log("Create Room Request Status: " + status);
                console.log(data);
            }
        }
    );
}
