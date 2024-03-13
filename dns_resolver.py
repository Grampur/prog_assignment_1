def parse_input_files(queries_file, cache_file, server_files):
    # Read DNS queries from dns-queries.txt
    with open(queries_file, 'r') as f:
        queries = [line.strip() for line in f.readlines()]

    # Read cache entries from cache-entries.txt
    with open(cache_file, 'r') as f:
        cache = [line.strip().split(';') for line in f.readlines()]

    # Read server mappings from server files
    server_mappings = {}
    for server_file in server_files:
        with open(server_file, 'r') as f:
            mappings = [line.strip().split(';') for line in f.readlines()]
            server_mappings[server_file] = mappings

    return queries, cache, server_mappings


class DNSCache:
    def __init__(self, initial_entries):
        self.cache = initial_entries[:3]  # Keep only the first 3 entries

    def get(self, domain):
        # Check if the domain is in the cache
        for entry in self.cache:
            if entry[0] == domain:
                self.cache.remove(entry)  # Remove the entry from its current position
                self.cache.append(entry)  # Add it to the end (most recent)
                return entry[1]  # Return the IP address
        return None

    def add(self, domain, ip_address):
        # If the cache is full, remove the oldest entry
        if len(self.cache) == 3:
            self.cache.pop(0)

        # Add the new entry as the most recent
        self.cache.append([domain, ip_address])


def resolve_query(query, server_mappings, cache):
    visited_servers = ['1-0-0-0']  # Start from the root server
    current_server = '1-0-0-0.txt'

    while True:
        # Check if the query can be resolved from the current server
        for mapping in server_mappings[current_server]:
            domain, ip_address = mapping

            if query.endswith(domain):
                # Update the cache with the resolved query
                cache.add(query, ip_address)

                # Print the visited servers and the resolved IP address
                print(';'.join(visited_servers + [ip_address]))
                print(f'{query};{ip_address}')
                return

        # Find the next server to visit
        found_next_server = False
        for mapping in server_mappings[current_server]:
            domain, ip_address = mapping
            if query.endswith('.' + domain):
                visited_servers.append(ip_address)
                current_server = f'{ip_address}.txt'
                found_next_server = True
                break

        if not found_next_server:
            # Unable to resolve the query
            print('Unresolved')
            return

        # If we reach this point, it means we need to follow a sub-domain
        for mapping in server_mappings[current_server]:
            domain, ip_address = mapping
            if domain in query:
                current_server = f'{ip_address}.txt'
                found_next_server = True
                break

        if not found_next_server:
            # Unable to resolve the query
            print('Unresolved')
            return


def main():
    queries_file = 'dns-queries.txt'
    cache_file = 'cache-entries.txt'
    server_files = ['1-0-0-0.txt', '1-0-0-1.txt', '100-200-25-35.txt', '50-50-40-66.txt']

    queries, initial_cache, server_mappings = parse_input_files(queries_file, cache_file, server_files)
    cache = DNSCache(initial_cache)

    for query in queries:
        print(f'Resolving query: {query}')
        if cache.get(query):
            print('cache')
            print(f'{query};{cache.get(query)}')
        else:
            resolve_query(query, server_mappings, cache)

    print('Current cache:')
    for entry in cache.cache:
        print(f'{entry[0]};{entry[1]}')


if __name__ == '__main__':
    main()