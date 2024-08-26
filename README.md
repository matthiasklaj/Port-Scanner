# Asynchronous Network Port Scanner

This project provides an asynchronous network port scanner written in Python, designed to efficiently scan a range of ports on a given host. It leverages Python's `asyncio` library to handle network operations concurrently, making it suitable for scanning multiple ports or hosts without significant delays.

## Features

- **Asynchronous Scanning:** Utilizes `asyncio` for non-blocking network operations, improving performance.
- **TCP and UDP Support:** Supports scanning both TCP and UDP ports.
- **Customizable Timeout:** Allows setting a timeout for socket operations to balance between speed and reliability.

## Installation

Ensure you have Python 3.7 or higher installed. No additional packages are required beyond the standard library.

## Usage

You can run the port scanner from the command line. Here’s the syntax:

```bash
python port_scanner.py <host> <port1> <port2> ... [--protocol <tcp|udp>]
