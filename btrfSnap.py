import argparse
import pathlib
import subprocess

#####################
# TTL Management
class TTL:
    def __init__(self,Years, Months, Weeks, Days, Hours, Minutes, Seconds):
        self.years = Years
        self.months = Months
        self.weeks = Weeks
        self.days = Days
        self.hours = Hours
        self.minutes = Minutes
        self.seconds = Seconds
    
    def __str__(self):
        return f"{self.years}y{self.months}m{self.weeks}w{self.days}d{self.hours}h{self.minutes}M{self.seconds}s"

    @staticmethod
    def from_str(str):
        curr = ""
        
        accumulate = []

        for index,item in enumerate(str, start=0):
            if (item.isdigit()):
                curr += item
            elif (item.isalpha()):
                num = int(curr)
                tag = item
                accumulate.append((num, tag))
                curr = ""
            else:
                raise ValueError

        TTL_toret = TTL(0,0,0,0,0,0,0)

        for item in accumulate:
            match item[1]:
                case 'y':
                    if (TTL_toret.years != 0):
                        raise ValueError
                    TTL_toret.years = int(item[0])
                case 'm':
                    if (TTL_toret.months != 0):
                        raise ValueError
                    TTL_toret.months = int(item[0])
                case 'w':
                    if (TTL_toret.weeks != 0):
                        raise ValueError
                    TTL_toret.weeks = int(item[0])
                case 'd':
                    if (TTL_toret.days != 0):
                        raise ValueError
                    TTL_toret.days = int(item[0])
                case 'h':
                    if (TTL_toret.hours != 0):
                        raise ValueError
                    TTL_toret.hours = int(item[0])
                case 'M':
                    if (TTL_toret.minutes != 0):
                        raise ValueError
                    TTL_toret.minutes = int(item[0])
                case 's':
                    if (TTL_toret.seconds != 0):
                        raise ValueError
                    TTL_toret.seconds = int(item[0])
        return TTL_toret
                

def test_TTL():
    str = "1y3m2w8d10h3M10s"
    new_str = TTL.from_str(str)
    print(new_str)

#test_TTL()

#####################
# Individual Commands

## List
def handle_list(parsed_args):
    if parsed_args.verbose:
        print(f"Listing snapshots for path: {parsed_args.btrfs_path}")

    cmd = f"btrfs subvolume list -s {parsed_args.btrfs_path}"
    subprocess.run(cmd, shell=True)

## Destroy
def handle_destroy(parsed_args):
    print('handling destroy')

## Create
def handle_create(parsed_args):
    if parsed_args.verbose:
        print(f"Creating snapshot for path: {parsed_args.btrfs_path}")

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
                    help="TTL formatted automatic lifetime for the snapshot.  Defaults to 1m.  See TTL definition")
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
    print(f"Parsed Args into: {parsed}")

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
