<template>

<div class="container">
		<div class="jumbotron vertical-center">
			
			<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/lux/bootstrap.min.css" 
			integrity="sha384-9+PGKSqjRdkeAU7Eu4nkJU8RFaH8ace8HGXnkiKMP9I9Te0GJ4/km3L1Z8tXigpG" crossorigin="anonymous">
			
			<div class="row">
				<div class="col-sm-12">
					<h2 class="text-center bg-primary text-white">Vote</h2>
					<hr><br>
					
					<table class="table table-hover">
						<thead>
							<tr>
								<th scope="col">Name</th>
								<th scope="col">Description</th>
								<th scope="col">Number of Positions</th>
								<th scope="col">Begins</th>
								<th scope="col">Ends</th>
								<th scope="col">Fingerprint</th>
								<th scope="col">Actions</th>
							</tr>
						</thead>
						<tbody>
							<tr v-for="election, index in elections" :key="index">
								<td>{{ election.Name }}</td>
								<td>{{ election.Description }}</td>
								<td>{{ election.Quantity }}</td>
								<td>{{ election.StartDate }} {{ election.StartTime }}</td>
								<td>{{ election.EndDate }} {{ election.EndTime }}</td>
								<td>{{ election.Fingerprint }}</td>
								<td>
									<div class="btn-group" role="group">
										<button type="button" class="btn btn-success btn-sm" v-b-modal.authenticate-vote>Vote</button>	
									</div>
								</td>
							</tr>
						</tbody>
					</table>
					<footer class="bg-primary text-white text-center" style="border-radius: 10px;">Copyright &copy;. All Rights Reserved 2023.</footer>
				</div>
			</div>

			<b-modal ref="authenticateVote" id="authenticate-vote" title="Authentication" hide-backdrop hide-footer>
				<b-form @submit="onSubmitAuth" @reset="onResetAuth" class="w-100 text-center">
					
					<b-form-group id="form-auth-pswd-group" label="Password" label-for="form-auth-pswd-input">
						<b-form-input id="form-auth-pswd-input" 
									type="text" 
									v-model="authVoteElectionForm.Password" 
									required 
									placeholder="Enter your master password...">
						</b-form-input>
					</b-form-group>

					<b-form-group id="form-auth-id-group" label="Voter ID" label-for="form-auth-id-input">
						<b-form-input id="form-auth-id-input" 
									type="text" 
									v-model="authVoteElectionForm.ID" 
									required 
									placeholder="Enter the voter's unique ID...">
						</b-form-input>
					</b-form-group>

					<b-button type="submit" variant="outline-success">Authenticate</b-button>
					<b-button type="reset" variant="outline-danger">Cancel</b-button>

				</b-form>
			</b-modal>

			<b-modal ref="votingModal" id="vote-modal" title="Enter your vote" hide-footer>
					<!-- <b-form @submit="onSubmit" @reset="onReset" class="w-100 text-center"> -->

				<div class="urn-keyboard">

					<div class="alphanumeric">
						<div class="alphanumeric-row">
							<button v-on:click="addNumber(1)">1</button>
							<button v-on:click="addNumber(2)">2</button>
							<button v-on:click="addNumber(3)">3</button>
						</div>

						<div class="alphanumeric-row">
							<button v-on:click="addNumber(4)">4</button>
							<button v-on:click="addNumber(5)">5</button>
							<button v-on:click="addNumber(6)">6</button>
						</div>

						<div class="alphanumeric-row">
							<button v-on:click="addNumber(7)">7</button>
							<button v-on:click="addNumber(8)">8</button>
							<button v-on:click="addNumber(9)">9</button>
						</div>

						<div class="alphanumeric-row">
							<button v-on:click="addNumber(0)">0</button>
						</div>
					</div>

					<div class="urn-keyboard-actions">
						<b-button class="btn btn-light" v-on:click="blankVote()">BLANK</b-button>
						<b-button class="btn btn-warning" v-on:click="reviseVote()">REVISE</b-button>
						<b-button class="btn btn-success" v-on:click="confirmVote()">CONFIRM</b-button>
					</div>
				</div>

			</b-modal>
		</div>
	</div>
</template>

<script>
import axios from 'axios';

export default {
	data() {
		return {
			elections: [],
			authVoteElectionForm: {
				'Password': '',
				'ID': ''
			}
		};
	},
	methods: {
		getElections() {
			const path = 'http://localhost:5000/voting';
			axios.get(path)
			.then((res) => {
				this.elections = res.data.elections;
				console.log(this.elections);
			})
			.catch((err) => {
				alert(err);
			});
		},
		clearPswd() {
			this.authVoteElectionForm.Password = '';
			this.authVoteElectionForm.ID = '';
		},
		onSubmitAuth(e) {
			e.preventDefault();
			const payload = {
				Password: this.authVoteElectionForm.Password
			};
			this.authenticateBoardMember(payload);
			this.clearPswd();
		},
		onResetAuth(e) {
			e.preventDefault();
			this.$refs.authenticateEdit.hide();
			this.clearPswd();
		},
		authenticateBoardMember(payload) {
			const path = 'http://localhost:5000/voting';
			axios.post(path, payload)
			.then((res) => {
				if (res.data['status'] == 'success') {
					this.$refs.authenticateVote.hide();
					this.$refs.votingModal.show();
				}
			})
			.catch((err) => {
				alert(err);
				this.getElections();
			});
		}
	},
	created() {
		this.getElections();
	}
};
</script>

<style scoped>
::v-deep #vote-modal > .modal-dialog {
	max-width: 80%;
	max-height: 100%;
} 
/* TODO: Clean keyboard stylization */
.urn-keyboard {
	margin: 0 auto;
	width: 40%;
	height: 100%;
	border-radius: 5px;
	padding: 20px;
	display: flex;
	flex-direction: column;
	justify-content: space-around;
}
.alphanumeric {
	width: 100%;
}
.alphanumeric-row {
	display: flex;
	justify-content: space-around;
	margin-bottom: 20px;
}
.alphanumeric button {
	background-color: #4b4242;
	color: #ffffff;
	font-size: 30px;
	border-radius: 5px;
	width: 80px;
	height: 50px;
}
.urn-keyboard-actions {
	width: 100%;
	display: flex;
	justify-content: space-around;
}
.urn-keyboard-actions button {
	border: 2px solid #756b6b;
	font-size: 15px;
	border-radius: 5px;
	width: 30%;
	height: 50px;
}
@media (max-width: 900px) {
.alphanumeric button {
	width: 58px;
	height: 34px;
	font-size: 20px;
}
.urn-keyboard-actions button {
	font-size: 9px;
	font-weight: bold;
	width: 30%;
	height: 35px;
}
}
h2 {
	padding: 15px;
	border-radius: 10px;
}
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>