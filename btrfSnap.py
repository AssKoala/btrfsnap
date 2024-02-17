import argparse
import pathlib
import subprocess

#####################
# Individual Commands

## List
def handle_list(parsed_args):
    print('Listing snapshots for path: {}'.format(parsed_args.btrfs_path))

    cmd = "btrfs subvolume list -s {}".format(parsed_args.btrfs_path)
    subprocess.run(cmd, shell=True)

## Destroy
def handle_destroy(parsed_args):
    print('handling destroy')

## Create
def handle_create(parsed_args):
    print('handling create')

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

# Path to run on
parser.add_argument('btrfs_path', type=pathlib.Path,
                    help='btrfs path, e.g. /mnt/btrfs')

try:
    result = parser.parse_args()
    print(result)
except:
    print("Exception occurred")
    exit(-1)

match result.btrfs_command:
    case "list":
        handle_list(result)
    case "destroy":
        handle_destroy(result)
    case "create":
        handle_create(result)
    case _:
        print("invalid command")
        exit(-1)
