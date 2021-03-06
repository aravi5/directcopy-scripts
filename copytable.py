#!/usr/bin/python

# Created by aravi

import sys
import logging
import argparse
from threading import Thread, Lock
import utils
import config

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s', )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    sub_parsers = parser.add_subparsers(help='command',
                                        dest='cmd_name')

    # create command
    create_parser = sub_parsers.add_parser('copytable',
                                           help='Tool to create copy of a table in MapRDB-JSON')
    create_sub_parser = create_parser.add_subparsers(help='type',
                                                     dest='obj_type')

    # create table command
    create_table_parser = create_sub_parser.add_parser('table',
                                                       help='Create table / tables')
    create_table_parser.add_argument('-prefix',
                                     help='Prefix for table path',
                                     required=True)
    create_table_parser.add_argument('-numtables',
                                     type=int,
                                     default=1,
                                     help='Number of tables (default: 1)')
    create_table_parser.add_argument('-startidx',
                                     type=int,
                                     default=1,
                                     help='Start index of table (default: 1)')

    # create volume command
    create_vol_parser = create_sub_parser.add_parser('volume',
                                                     help='Create volume / volumes')
    create_vol_parser.add_argument('-prefix',
                                   help='Prefix for volume path',
                                   required=True)
    create_vol_parser.add_argument('-numvolumes',
                                   type=int,
                                   default=1,
                                   help='Number of volumes (default: 1)')
    create_vol_parser.add_argument('-startidx',
                                   type=int,
                                   default=1,
                                   help='Start index of volume (default: 1)')

    # delete command
    delete_parser = sub_parsers.add_parser('delete',
                                           help='Delete table(s) / volume(s)')
    delete_sub_parser = delete_parser.add_subparsers(help='type',
                                                     dest='obj_type')

    # delete table command
    delete_table_parser = delete_sub_parser.add_parser('table',
                                                       help='Delete table / tables')
    delete_table_parser.add_argument('-prefix',
                                     help='Prefix for table path',
                                     required=True)
    delete_table_parser.add_argument('-numtables',
                                     type=int,
                                     default=1,
                                     help='Number of tables (default: 1)')
    delete_table_parser.add_argument('-startidx',
                                     type=int,
                                     default=1,
                                     help='Start index of table (default: 1)')

    # delete volume command
    delete_vol_parser = delete_sub_parser.add_parser('volume',
                                                     help='Delete volume / volumes')
    delete_vol_parser.add_argument('-prefix',
                                   help='Prefix for volume path',
                                   required=True)
    delete_vol_parser.add_argument('-numvolumes',
                                   type=int,
                                   default=1,
                                   help='Number of volumes (default: 1)')
    delete_vol_parser.add_argument('-startidx',
                                   type=int,
                                   default=1,
                                   help='Start index of volume (default: 1)')

    # autopsetup command
    autosetup_parser = sub_parsers.add_parser('autosetup',
                                              help='Autosetup replica for table / tables in volume')
    autosetup_sub_parser = autosetup_parser.add_subparsers(help='type',
                                                           dest='obj_type')

    # autosetup table command
    autosetup_table_parser = autosetup_sub_parser.add_parser('table',
                                                             help='Create autosetup for a table')
    autosetup_table_parser.add_argument('-path',
                                        help='Source table path',
                                        required=True)
    autosetup_table_parser.add_argument('-replica',
                                        help='Path to parent directory of replica table',
                                        required=True)
    autosetup_table_parser.add_argument('-numreplica',
                                        type=int,
                                        default=1,
                                        help='Number of replicas (default: 1)')
    autosetup_table_parser.add_argument('-multimaster',
                                        action='store_true',
                                        help="Multimaster if specified")

    # autosetup volume command
    autosetup_vol_parser = autosetup_sub_parser.add_parser('volume',
                                                           help='Create autosetup for tables in a volume')
    autosetup_vol_parser.add_argument('-path',
                                      help='Volume path',
                                      required=True)
    autosetup_vol_parser.add_argument('-replica',
                                      help='Path to parent directory of replica table',
                                      required=True)
    autosetup_vol_parser.add_argument('-numreplica',
                                      type=int,
                                      default=1,
                                      help='Number of replicas (default: 1)')
    autosetup_vol_parser.add_argument('-multimaster',
                                      action='store_true',
                                      help="Multimaster is specified")

    # load command
    load_parser = sub_parsers.add_parser('load',
                                         help='load data on to table / tables in volume')
    load_sub_parser = load_parser.add_subparsers(help='type',
                                                 dest='obj_type')

    # load table command
    load_table_parser = load_sub_parser.add_parser('table',
                                                   help='Load data on to a table')
    load_table_parser.add_argument('-path',
                                   help='Path of the table',
                                   required=True)
    load_table_parser.add_argument('-numcfs',
                                   type=int,
                                   default=1,
                                   help='Number of CFs to create (default: 1)')
    load_table_parser.add_argument('-numcols',
                                   type=int,
                                   default=3,
                                   help='Number of columns (default: 3)')
    load_table_parser.add_argument('-numrows',
                                   type=int,
                                   default=100000,
                                   help='Number of rows to insert (default: 100000)')
    load_table_parser.add_argument('-json',
                                   action='store_true',
                                   help="Json table if specified")

    # load tables in volume command
    load_volume_parser = load_sub_parser.add_parser('volume',
                                                    help='Load data on to tables in a volume')
    load_volume_parser.add_argument('-path',
                                    help='Volume path ',
                                    required=True)
    load_volume_parser.add_argument('-numcfs',
                                    type=int,
                                    default=1,
                                    help='Number of CFs to create (default: 1)')
    load_volume_parser.add_argument('-numcols',
                                    type=int,
                                    default=3,
                                    help='Number of columns (default: 3)')
    load_volume_parser.add_argument('-numrows',
                                    type=int,
                                    default=100000,
                                    help='Number of rows to insert (default: 100000)')
    load_volume_parser.add_argument('-json',
                                    action='store_true',
                                    help="Json table if specified")

    # track replica command
    repl_parser = sub_parsers.add_parser('replstatus',
                                         help='Track replica status of table / tables in a volume')
    repl_sub_parser = repl_parser.add_subparsers(help='type',
                                                 dest='obj_type')

    # track replica table command
    repl_table_parser = repl_sub_parser.add_parser('table',
                                                   help='Track replica of a table')
    repl_table_parser.add_argument('-path',
                                   help='Path of the table',
                                   required=True,
                                   type=str)
    repl_table_parser.add_argument('-filter',
                                   help='Filter required fields (comma separated)',
                                   type=str)

    # track replica volume command
    repl_vol_parser = repl_sub_parser.add_parser('volume',
                                                 help='Track replica of tables in a volume')
    repl_vol_parser.add_argument('-path',
                                 help='Path of the volume',
                                 required=True,
                                 type=str)
    repl_vol_parser.add_argument('-filter',
                                 help='Filter required fields (comma separated)',
                                 type=str)

    # execute stress profile
    stress_parser = sub_parsers.add_parser('stress',
                                           help='Stress reliable replication')
    stress_sub_parser = stress_parser.add_subparsers(help='Type of stress profile',
                                                     dest='obj_type')
    # bulk stress profile
    stress_bulk_parser = stress_sub_parser.add_parser('bulk',
                                                      help='Bulk profile of stress')

    # incremental stress profile
    stress_incr_parser = stress_sub_parser.add_parser('increment',
                                                      help='Incremental profile of stress')

    args = parser.parse_args()
    print args

    if args.cmd_name == 'create':
        logging.debug('Create command')
        if args.obj_type == 'table':
            utils.create_table(table_path_prefix=args.prefix,
                               start_idx=args.startidx,
                               num_tables=args.numtables)
        elif args.obj_type == 'volume':
            utils.create_volume(volume_path_prefix=args.prefix,
                                start_idx=args.startidx,
                                num_volumes=args.numvolumes)
        else:
            logging.error('Unrecognized object. Cannot create.')
            sys.exit(-1)
    elif args.cmd_name == 'delete':
        logging.debug('Delete command')
        if args.obj_type == 'table':
            utils.delete_table(table_path_prefix=args.prefix,
                               start_idx=args.startidx,
                               num_tables=args.numtables)
        elif args.obj_type == 'volume':
            utils.delete_volume(volume_path_prefix=args.prefix,
                                start_idx=args.startidx,
                                num_volumes=args.numvolumes)
        else:
            logging.error('Unrecognized object. Cannot create.')
            sys.exit(-1)
    elif args.cmd_name == 'autosetup':
        logging.debug('Autosetup command')
        if args.obj_type == 'table':
            utils.autosetup_replica_table(src_table=args.path,
                                          replica_parent=args.replica,
                                          num_replica=args.numreplica,
                                          is_multimaster=args.multimaster)
        elif args.obj_type == 'volume':
            utils.autosetup_replica_table_multithread(volume_path=args.path,
                                                      replica_parent=args.replica,
                                                      num_replica=args.numreplica,
                                                      is_multimaster=args.multimaster)
        else:
            logging.error('Unrecognized object. Cannot create.')
            sys.exit(-1)
    elif args.cmd_name == 'load':
        logging.debug('Load command')
        if args.obj_type == 'table':
            utils.load_table(table_name=args.path,
                             num_cfs=args.numcfs,
                             num_cols=args.numcols,
                             num_rows=args.numrows,
                             is_json=args.json)
        elif args.obj_type == 'volume':
            utils.load_volume_tables_multithread(volume_path=args.path,
                                                 num_cfs=args.numcfs,
                                                 num_cols=args.numcols,
                                                 num_rows=args.numrows,
                                                 is_json=args.json)
        else:
            logging.error('Unrecognized object. Cannot create.')
            sys.exit(-1)
    elif args.cmd_name == 'replstatus':
        logging.debug('Replica status tracking')
        if args.obj_type == 'table':
            utils.get_replica_status(table_name=args.path,
                                     fields=args.filter)
        elif args.obj_type == 'volume':
            utils.get_replica_status_multithread(volume_path=args.path,
                                                 fields=args.filter)
        else:
            logging.error('Unrecognized object. Cannot create.')
            sys.exit(-1)

    elif args.cmd_name == 'stress':
        logging.debug('Executing stress profile')
        if args.obj_type == 'bulk':
            execute_stress_bulk()
        elif args.obj_type == 'increment':
            execute_stress_incremental()
