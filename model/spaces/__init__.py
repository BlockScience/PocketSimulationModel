from .Servicer import (
    servicer_stake_space,
    servicer_pause_space,
    servicer_unpause_space,
    assign_servicer_salary_space,
    modify_servicer_pokt_space,
    servicer_param_update_space,
    servicer_unstake_space,
    servicer_unpause_space2,
    servicer_pause_space2,
    servicer_relay_space,
    return_servicer_stake_space,
    servicer_block_reward_space,
    servicer_stake_burn_space,
    servicer_forced_unstake_space,
    servicer_stake_status_space,
    remove_servicer_space,
    servicer_join_space,
    servicer_entity_space,
    service_linking_space
)
from .Application import (
    application_stake_space,
    modify_application_pokt_space,
    application_param_update_space,
    application_unstake_space,
    application_delegate_to_portal_space,
    application_undelegation_space,
    submit_relay_request_space,
    return_application_stake_space,
    application_stake_status_space,
    application_join_space,
    application_entity_space,
)
from .Validator import (
    validator_stake_space,
    modify_validator_pokt_space,
    validator_param_update_space,
    validator_pause_space,
    validator_stake_burning_space,
    validator_block_reward_space,
)
from .Portal import (
    portal_registration_space,
    portal_unregistration_space,
    portal_relay_request_space,
    modify_portal_pokt_space,
    portal_stake_status_space,
    return_portal_stake_space,
    portal_join_space,
    portal_entity_space
)
from .Treasury import (
    mint_block_rewards_space,
    burn_pokt_space,
    jail_node_space,
    mint_pokt_mechanism_space,
    burn_pokt_mechanism_space,
    increase_relay_fees_space,
    distribute_fees_space,
    decrease_relay_fees_space,
)
from .Node import unjail_node_space
from .Service import service_join_space, service_leave_space, service_entity_space
from .DAO import dao_block_reward_space, modify_dao_pokt_space

spaces = {
    "Servicer Stake Space": servicer_stake_space,
    "Servicer Pause Space": servicer_pause_space,
    "Servicer Pause Space 2": servicer_pause_space2,
    "Servicer Unpause Space": servicer_unpause_space,
    "Assign Servicer Salary Space": assign_servicer_salary_space,
    "Modify Servicer POKT Space": modify_servicer_pokt_space,
    "Servicer Param Update Space": servicer_param_update_space,
    "Servicer Unstake Space": servicer_unstake_space,
    "Application Stake Space": application_stake_space,
    "Servicer Unpause Space 2": servicer_unpause_space2,
    "Modify Application POKT Space": modify_application_pokt_space,
    "Application Param Update Space": application_param_update_space,
    "Application Unstake Space": application_unstake_space,
    "Application Delegate to Portal Space": application_delegate_to_portal_space,
    "Validator Stake Space": validator_stake_space,
    "Modify Validator POKT Space": modify_validator_pokt_space,
    "Validator Param Update Space": validator_param_update_space,
    "Portal Registration Space": portal_registration_space,
    "Portal Unregistration Space": portal_unregistration_space,
    "Application Undelegation Space": application_undelegation_space,
    "Validator Pause Space": validator_pause_space,
    "Validator Stake Burning Space": validator_stake_burning_space,
    "Validator Block Reward Space": validator_block_reward_space,
    "Submit Relay Request Space": submit_relay_request_space,
    "Servicer Relay Space": servicer_relay_space,
    "Mint Block Rewards Space": mint_block_rewards_space,
    "Burn POKT Space": burn_pokt_space,
    "Jail Node Space": jail_node_space,
    "Unjail Node Space": unjail_node_space,
    "Return Servicer Stake Space": return_servicer_stake_space,
    "Service Join Space": service_join_space,
    "Service Leave Space": service_leave_space,
    "Return Application Stake Space": return_application_stake_space,
    "Servicer Block Reward Space": servicer_block_reward_space,
    "Mint POKT Mechanism Space": mint_pokt_mechanism_space,
    "Burn POKT Mechanism Space": burn_pokt_mechanism_space,
    "DAO Block Reward Space": dao_block_reward_space,
    "Modify DAO POKT Space": modify_dao_pokt_space,
    "Portal Relay Request Space": portal_relay_request_space,
    "Servicer Stake Burn Space": servicer_stake_burn_space,
    "Servicer Forced Unstake Space": servicer_forced_unstake_space,
    "Servicer Stake Status Space": servicer_stake_status_space,
    "Application Stake Status Space": application_stake_status_space,
    "Modify Portal POKT Space": modify_portal_pokt_space,
    "Portal Stake Status Space": portal_stake_status_space,
    "Return Portal Stake Space": return_portal_stake_space,
    "Increase Relay Fees Space": increase_relay_fees_space,
    "Distribute Fees Space": distribute_fees_space,
    "Decrease Relay Fees Space": decrease_relay_fees_space,
    "Remove Servicer Space": remove_servicer_space,
}