import argparse
import pathlib
import subprocess

#####################
# Individual Commands

## List
def handle_list(parsed_args):
    if parsed_args.verbose:
        print('Listing snapshots for path: {}'.format(parsed_args.btrfs_path))

    cmd = "btrfs subvolume list -s {}".format(parsed_args.btrfs_path)
    subprocess.run(cmd, shell=True)

## Destroy
def handle_destroy(parsed_args):
    print('handling destroy')

## Create
def handle_create(parsed_args):
    if parsed_args.verbose:
        print('Creating snapshot for path: {}'.format(parsed_args.btrfs_path))



#####################
# Main

# Initialize command line parsing
parser = argparse.ArgumentParser(
    prog='btrfSnap',
    description='btrfs snapshot helper scripts, inspired by zfSnap',
    exit_on_error=False)

# global opts
parser.add_argument('-b', '--btrfs-cmd-path',
                    required=False,
                    type=pathlib.Path)
parser.add_argument('-n', '--dry-run',
                    required=False,
                    action='store_true')
parser.add_argument('-v', '--verbose', 
                    action='store_true',
                    required=False,
                    help='Enable verbose output from script and btrfs when possible')

# Commands
parser.add_argument('btrfs_command', 
                    choices=['list', 'destroy', 'create'], 
                    help='Commands to execute')

# Create options
parser.add_argument('-r', '--read-only',
                    action='store_true',
                    required=False,
                    default=True,
                    help='Marks the snapshot as read only. Defaults to True')
parser.add_argument('-s','--snapshot-folder',
                    required=False,
                    default='.snapshot',
                    help="Folder to place the snapshot in. Defaults to $PATH/.snapshot",
                    type=pathlib.Path)
parser.add_argument('-a','--automatic-lifetime',
                    required=False,
                    default='1m',
                    help="Automatic lifetime for the snapshot.  Defaults to 1m")
parser.add_argument('-p', '--prefix',
                    required=False,
                    help="Prefix to prepend to snapshot names (e.g. MyPrefix-1m)")

# Path to run on
parser.add_argument('btrfs_path', type=pathlib.Path,
                    help='btrfs path, e.g. /mnt/btrfs')

try:
    parsed = parser.parse_args()
    print(parsed)
except:
    print("Exception occurred")
    exit(-1)

if parsed.verbose:
    print('Parsed Args into: {}'.format(parsed))

match parsed.btrfs_command:
    case "list":
        handle_list(parsed)
    case "destroy":
        handle_destroy(parsed)
    case "create":
        handle_create(parsed)
    case _:
        print("invalid command")
        exit(-1)
