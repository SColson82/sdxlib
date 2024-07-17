from sdxlib.sdx_client import SDXClient
from sdxlib.sdx_exception import SDXException

if __name__ == "__main__":
    # Example usage
    client_name = "Test L2VPN"
    client_endpoints = [
        {
            "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
            "vlan": "100",
        },
        {
            "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
            "vlan": "200",
        },
    ]
    client_description = (
        ""  # This is an example to demonstrate a L2VPN with optional attributes."
    )
    client_notifications = []  #{"email":f"user{i+1}@email.com"} for i in range(10)]
    client_scheduling = {
        "start_time": "2024-07-04T10:00:00Z",
        "end_time": "2024-07-05T18:00:00Z"
    }
    client_qos_metrics = {
        # "min_bw": {
        # "value": 5,
        # "strict": False
        # },
        # "max_delay": {
        #     "value": 150,
        #     "strict": True
        # },
        # "max_number_oxps": {
        #     "value": 100,
        #     "strict": True
        # }
    }

    client = SDXClient(
        base_url="http://example.com",
        name=client_name,
        endpoints=client_endpoints,
        description=client_description,
        notifications=client_notifications,
        scheduling=client_scheduling,
        qos_metrics=client_qos_metrics,
    )

    try:
        print(client.name)
        print(client.endpoints)
        print(client.description)
        print(client.notifications)
        print(client.scheduling)
        print(client.qos_metrics)
    except ValueError as e:
        print(f"Error: {e}")
    except TypeError as e:
        print(f"Error: {e}")
    except SDXException as e:
        print(f"SDX Error: {e.status_code} - {e.message}")

    # try:
    #     response = client.create_l2vpn()
    #     print(response)
    # except SDXException as e:
    #     print(e.message)

    # try:
    #     response = client.update_l2vpn("123e4567-e89b-12d3-a456-426614174000", "state", "enabled")
    #     print("Update Successful:", response)
    # except SDXException as e:
    #     print(e.message)

    # # Update description
    # response_json = client.update_l2vpn(
    #     "123e4567-e89b-12d3-a456-426655440000", "description", "New description"
    # )

    # # Enable the L2VPN
    # response_json = client.update_l2vpn(
    #     "123e4567-e89b-12d3-a456-426655440000", "state", "enabled"
    # )

    # # Try updating an invalid attribute (service_id)
    # try:
    #     response_json = client.update_l2vpn(
    #         "123e4567-e89b-12d3-a456-426655440001", "service_id", "new-id"
    #     )
    # except ValueError

    # client = SDXClient(base_url="http://example.com")
    # try:
    #     l2vpns = client.get_all_l2vpns("2023-07-16T19:20:30Z")
    #     print(l2vpns)
    # except ValueError as e:
    #     print(f"Validation error: {e}")
    # except SDXException as e:
    #     print(f"SDX error: {e}")