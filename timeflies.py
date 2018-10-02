import cProfile
import pstats
import sys
import time
from contextlib import ContextDecorator
from inspect import getframeinfo, stack

import crayons
import io


__version__ = '0.0.1'


def better_func_name(x):
    if x[0] == '~':
        return '(built-in)'
    if '/site-packages/' in x:
        return x.split('site-packages/')[1]
    if 'lib/python' in x:
        return x.split('lib/')[1]
    return crayons.yellow("/".join(x.split('/')[-3:]), always=True)


def strip_long(x):
    x = x.replace("\n", " ")
    max_length = 120
    if len(x) <= max_length+3:
        return x

    return x[0:(max_length//2)] + '...' + x[-(max_length//2):]


class profile(ContextDecorator):
    def __init__(self, engine=None, smart=True, n=20):
        self.engine = engine
        self.smart = smart
        self.n = 20

    def before_cursor_execute(self, conn, cursor, statement, parameters, context, executemany):
        conn.info.setdefault('query_start_time', []).append(time.time())

    def after_cursor_execute(self, conn, cursor, statement, parameters, context, executemany):
        total = time.time() - conn.info['query_start_time'].pop(-1)
        self.queries.append((total, statement))

    def print_line(self, ps, func):
        cc, nc, tt, ct, callers = ps.stats[func]
        print('%s %s %s %s:%s %s' % (
            str(round(ct, 4)).ljust(8),
            str(round(tt, 4)).ljust(8),
            str(cc).ljust(8),
            better_func_name(func[0]),
            func[1],
            crayons.green(func[2], always=True),
        ))

    def __enter__(self):
        # Try being smart and get the engine from Flask-SQLAlchemy
        if not self.engine and self.smart:
            try:
                from flask import current_app
                self.engine = current_app.extensions['sqlalchemy'].db.engine
            except Exception as e:
                pass

        self.queries = []
        self.caller = None
        for val in stack()[1:]:
            frame = getframeinfo(val[0])
            if not frame.filename.endswith('contextlib.py'):
                self.caller = frame
                break
        self.pr = cProfile.Profile()
        self.pr.enable()

        if self.engine:
            import sqlalchemy

            sqlalchemy.event.listen(self.engine, "before_cursor_execute", self.before_cursor_execute)
            sqlalchemy.event.listen(self.engine, "after_cursor_execute", self.after_cursor_execute)
        return self

    def __exit__(self, *exc):
        self.pr.disable()
        if self.engine:
            import sqlalchemy

            sqlalchemy.event.remove(self.engine, "before_cursor_execute", self.before_cursor_execute)
            sqlalchemy.event.remove(self.engine, "after_cursor_execute", self.after_cursor_execute)

        s = io.StringIO()
        ps = pstats.Stats(self.pr, stream=s).sort_stats('cumulative')
        if ps.total_tt < 1:
            time_spent = crayons.green(str(round(ps.total_tt, 3)), always=True)
        else:
            time_spent = crayons.red(str(round(ps.total_tt, 3)), always=True)

        print('⏳  Benchmarking started at %s:%d and finished in %s seconds' % (
            crayons.yellow(self.caller.filename, always=True) if self.caller else 'N/A',
            self.caller.lineno,
            time_spent
        ))
        print('')
        print('🔝  Most time spent cumulatively inside:')

        width, listd = ps.get_print_list([])
        print('%s %s %s %s' % (
            'cumtime'.ljust(8),
            'total'.ljust(8),
            'N'.ljust(8),
            'file'.ljust(8),
        ))
        for func in listd[0:self.n]:
            cc, nc, tt, ct, callers = ps.stats[func]
            self.print_line(ps=ps, func=func)
            if ct < 0.05 and self.smart:
                print('... not showing small functions')
                break

        print('')
        print('🔝  Most time in total:')

        ps.sort_stats('tottime')
        width, listd = ps.get_print_list([])
        print('%s %s %s %s' % (
            'cumtime'.ljust(8),
            'total'.ljust(8),
            'N'.ljust(8),
            'file'.ljust(8),
        ))
        for func in listd[0:self.n]:
            cc, nc, tt, ct, callers = ps.stats[func]
            self.print_line(ps=ps, func=func)
            if ct < 0.05 and self.smart:
                print('... skipping small functions')
                break

        print('')

        if self.engine:
            print('📖  %i SQL queries:' % len(self.queries))
            for time_spent, query in sorted(self.queries, key=lambda x: x[0], reverse=True)[0:self.n]:
                print('%s %s' % (
                    str(round(time_spent, 4)).ljust(8),
                    strip_long(query)
                ))

        sys.stdout.flush()


if __name__ == '__main__':
    import random
    arr = []

    def first():
        for i in range(30):
            random.choice(arr)()

    def second():
        random.choice(arr)()

    def third():
        random.choice(arr)()

    arr.append(second)
    arr.append(third)
    arr.append(lambda: None)

    with profile():
        second()
        third()
        first()
