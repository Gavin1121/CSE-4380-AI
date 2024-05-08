import sys

from pathlib import Path


def calculate_likelihood(hypothesis, observation):
    observation_key = "cherry" if observation == "C" else "lime"
    return hypothesis[observation_key]


def update_posterior(hypotheses, observation):
    total_prob = sum(
        hypothesis["prior"] * calculate_likelihood(hypothesis, observation)
        for hypothesis in hypotheses.values()
    )
    for hypothesis in hypotheses.values():
        likelihood = calculate_likelihood(hypothesis, observation)
        hypothesis["prior"] = (hypothesis["prior"] * likelihood) / total_prob


def next_candy_probability(hypotheses, candy_type):
    return sum(hypothesis["prior"] * hypothesis[candy_type] for hypothesis in hypotheses.values())


def calculate_posterior(hypotheses, observations):
    """..."""
    with Path.open("result.txt", "w") as file:
        file.write(f"Observation sequence Q: {observations}\n")
        file.write(f"Length of Q: {len(observations)}\n\n")

        for index, observation in enumerate(observations):
            update_posterior(hypotheses, observation)
            file.write(f"After Observation {index + 1} = {observation}:\n\n")

            for h_name, h_data in hypotheses.items():
                file.write(f"P({h_name} | Q) = {h_data['prior']:.5g}\n")

            file.write(
                f"\nProbability that the next candy we pick will be C, given Q: "
                f"{next_candy_probability(hypotheses, 'cherry'):.5g}\n"
            )
            file.write(
                f"Probability that the next candy we pick will be L, given Q: "
                f"{next_candy_probability(hypotheses, 'lime'):.5g}\n\n"
            )


def main() -> None:
    """..."""
    observations = sys.argv[1] if len(sys.argv) > 1 else ""

    hypotheses = {
        "h1": {"prior": 0.10, "cherry": 1.00, "lime": 0.00},
        "h2": {"prior": 0.20, "cherry": 0.75, "lime": 0.25},
        "h3": {"prior": 0.40, "cherry": 0.50, "lime": 0.50},
        "h4": {"prior": 0.20, "cherry": 0.25, "lime": 0.75},
        "h5": {"prior": 0.10, "cherry": 0.00, "lime": 1.00},
    }

    calculate_posterior(observations, hypotheses)


if __name__ == "__main__":
    main()
