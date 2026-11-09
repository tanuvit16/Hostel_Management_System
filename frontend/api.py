
import requests

BASE_URL = "http://localhost:8080/api"

def request_api(endpoint, method="GET", data=None, params=None):
    try:
        url = f"{BASE_URL}/{endpoint}"

        response = requests.request(
            method=method,
            url=url,
            data=data,
            params=params,
            timeout=10
        )

        result = response.json()

        if response.status_code >= 400:
            return {
                "success": False,
                "message": result.get("message", "Server error")
            }

        return result

    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "message": "Java backend is not running. Start Main.java first."
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "message": "Server request timed out."
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }


def login(username, password):
    return request_api(
        "login", "POST",
        {"username": username, "password": password}
    )


def get_stats():
    return request_api("stats")


def get_students(search=""):
    return request_api("students", params={"search": search})


def add_student(data):
    return request_api("students", "POST", data)


def update_student(data):
    return request_api("students", "PUT", data)


def delete_student(student_id):
    return request_api(
        "students", "DELETE", {"student_id": student_id}
    )


def get_rooms():
    return request_api("rooms")


def add_room(data):
    return request_api("rooms", "POST", data)


def update_room(data):
    return request_api("rooms", "PUT", data)


def delete_room(room_id):
    return request_api("rooms", "DELETE", {"room_id": room_id})


def get_allocations():
    return request_api("allocations")


def allocate_room(data):
    return request_api("allocations", "POST", data)


def get_fees():
    return request_api("fees")


def add_fee(data):
    return request_api("fees", "POST", data)


def update_fee(data):
    return request_api("fees", "PUT", data)


def delete_fee(fee_id):
    return request_api("fees", "DELETE", {"fee_id": fee_id})
