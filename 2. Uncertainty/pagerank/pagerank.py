import os
import random
import re
import sys
import numpy as np
import math

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    # ranks = IT(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    if not corpus[page]:
        return {link : 1 / len(corpus) for link in corpus}
    
    model = {}
    for link in corpus:
        model[link] = (1 - damping_factor) / len(corpus)
        if link in corpus[page]:
            model[link] += damping_factor / len(corpus[page])

    return model

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialization
    random.seed()
    sample = random.choice(list(corpus.keys()))
    pagerank = {page : 0 for page in list(corpus.keys())}

    # Iteration
    for i in range(n):
        pagerank[sample] += 1
        model = transition_model(corpus, sample, damping_factor)
        population, weights = zip(*model.items())
        # sample = np.random.choice(population, p=weights, replace=True) # Slow
        sample = random.choices(population, weights=weights, k=1)[0]
    
    for k in pagerank:
        pagerank[k] /= n

    return pagerank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pagerank = {page : 1 / len(corpus) for page in corpus}
    newrank = {}
    epsilon = 0.001

    while True:
        for page in pagerank:
            sum = 0
            for page_link in corpus:
                if not corpus[page_link]:
                    sum += pagerank[page_link] / len(corpus)
                elif page in corpus[page_link]:
                    sum += pagerank[page_link] / len(corpus[page_link])

            newrank[page] = (1 - damping_factor) / len(corpus) + damping_factor * sum

        repeat = False
        for page in pagerank:
            if not math.isclose(newrank[page], pagerank[page], abs_tol=epsilon):
                repeat = True
            pagerank[page] = newrank[page]
        
        if not repeat:
            break

    return pagerank



if __name__ == "__main__":
    main()
