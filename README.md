# Tempo

Tempo is a simple tool to perform Side-Channel Timing Attacks over HTTP.

It looks on a username list and performs HTTP requests to determine which usernames could be potentially valid based on the simple response time. It works better on a uniform connection to the target.

## Getting Started

Tempo is a  simple Python script. Just launch it and supply all required parameters. Type python tempo -h for argument lists. 

In a nutshell, it requires a username list (or whatever input needs to be tested), form-data to be submitted and target URL. Custom HTTP Headers are optional and can be added as well. 

### Prerequisites

Search requires standard Python 2.7.X.

### Installing

For Python installation:

```
https://www.python.org/downloads/
```

## Usage

### Simple Usage

```
python tempo.py -u username-list.txt -U username-field -t 'https://sometarget.com' -p 'password=randompass&Submit=ok' -H 'X-Custom-Header: test'
```
Obs: First 10 entries in the username list should be invalid and they are used only for metrics collections.

## Versioning

No system versioning in place yet

## Authors

* **Ismael Goncalves** -  [Sharingsec](https://sharingsec.blogspot.com)

## License

Apache 2.0
