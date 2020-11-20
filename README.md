# TrotskyCraft Utils

A datapack containing utilities for the TrotskyCraft minecraft server. This datapack is generated with python using `mcpack`.

## Community Contribution Command Purchases (CCCP)

An admin shop which allows players to trade resources for a reward item. Items traded by players are moved to a "community chest" (which could be an input to a sorting system).
The intention being to allow for trading and progression without fostering capitalist tendancies. When paired with one of the many shop plugins to provide rewards such as beacons,
elytra, custom enchantments etc., this allows for an entirely centrally-managed economy while still providing progression for players.  

## Usage

Create a virtual environment

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Make changes and run `python main.py` to create the datpack in the `out/` directory. 

### Releasing

Build the datapack:

```
script/create_datpack
```

Create the zip

```
script/create_zip
```

Upload the release (requires `gh` cli tool and an authenticated user)

```
script/release
```
