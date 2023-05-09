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
						<tbody v-for="election, index in elections" :key="index">
							<tr v-if="inProgress(election)">
								<td>{{ election.Name }}</td>
								<td>{{ election.Description }}</td>
								<td>{{ election.Quantity }}</td>
								<td>{{ election.StartDate }} {{ election.StartTime }}</td>
								<td>{{ election.EndDate }} {{ election.EndTime }}</td>
								<td>{{ election.Fingerprint }}</td>
								<td>
									<div class="btn-group" role="group">
										<button type="button" class="btn btn-success btn-sm" v-b-modal.authenticate-vote 
										@click="informElection(election)">Vote</button>	
									</div>
								</td>
							</tr>
						</tbody>
					</table>
					<footer class="bg-primary text-white text-center" style="border-radius: 10px;">
						Copyright &copy;. All Rights Reserved 2023.
					</footer>
				</div>
			</div>

			<b-modal ref="authenticateVote" id="authenticate-vote" title="Authentication" hide-backdrop hide-footer>
				<b-form @submit="onSubmitAuth" @reset="onResetAuth" class="w-100 text-center">
					
					<b-form-group class="create-form-control" id="form-auth-pswd-group" label="Password" label-for="form-auth-pswd-input">
						<b-form-input id="form-auth-pswd-input" 
									type="password" 
									v-model="authVoteElectionForm.Password" 
									required 
									placeholder="Enter your master password...">
						</b-form-input>
						<span class="exclamation">
							<font-awesome-icon icon="fas fa-exclamation-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<span class="check">
							<font-awesome-icon icon="fas fa-check-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<b-small></b-small>
					</b-form-group>

					<b-form-group class="create-form-control" id="form-auth-id-group" label="Voter's ID" label-for="form-auth-id-input">
						<b-form-input id="form-auth-id-input"
									v-mask="'###.###.###-##'"
									v-model="authVoteElectionForm.ID" 
									required 
									placeholder="Enter the voter's unique ID...">
						</b-form-input>
						<span class="exclamation">
							<font-awesome-icon icon="fas fa-exclamation-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<span class="check">
							<font-awesome-icon icon="fas fa-check-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<b-small></b-small>
					</b-form-group>

					<b-button type="submit" variant="outline-success">Authenticate</b-button>
					<b-button type="reset" variant="outline-danger">Cancel</b-button>

				</b-form>
			</b-modal>

			<b-modal ref="votingModal" id="vote-modal" title="Enter your vote" hide-footer>
					<!-- <b-form @submit="onSubmit" @reset="onReset" class="w-100 text-center"> -->
				
				<div class="urna-tela">
					<div v-if="votingSession.Screen != 'end'" class="urna-tela-voto">
						<div class="urna-tela-voto-textos">
							<h2 class="urna-tela-voto-titulo">Your vote for: {{  votingSession.Screen }}</h2>
							<div class="each-number">
								<h2>Vote</h2>

								<div
									class="otp-box"
									v-for="(value, key) in votingSession.VoteChoice.padEnd(votingSession.DigitsQuantity, ' ')"
									:key="key"
								>
									{{ value }}
								</div>
							</div>

							<hr>
							<div class="urna-tela-voto-descricao">
								Name:<strong> {{ votingSession.candidate.Name ? votingSession.candidate.Name : "________" }} </strong>
							</div>

							<div class="urna-tela-voto-descricao">
								Party:<strong>{{ votingSession.candidate.Party ? votingSession.candidate.Party : " ________" }}</strong>
							</div>

						</div>
					</div>
					<div v-if="votingSession.Screen == 'end'" class="urna-tela-fim">FIM</div>
				</div>

				<hr>
				<br><br>

				<div v-if="votingSession.Screen != 'end'" class="urn-keyboard">

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
import confirmAudio from '../assets/confirm.wav';
import keyAudio from '../assets/key.wav';

export default {
	data() {
		return {
			elections: [],
			authVoteElectionForm: {
				'Password': '',
				'ID': '',
				'ElectionID': ''
			},
			votingSession: {
				'DigitsQuantity': 0,
				'VoteChoice': '',
				'Screen': '',
				candidate: {
					'Name': '',
					'Party': ''
				}
			},
			electionData: [],
			voteID: '',
			postVote: [],
			digits: [],
			steps: []
		};
	},
	
	methods: {
		getElections() {
			const path = 'http://localhost:5000/voting';
			axios.get(path)
			.then((res) => {
				this.elections = res.data.elections;
			})
			.catch((err) => {
				alert(err);
			});
		},

		clearPswd() {
			this.authVoteElectionForm.Password = '';
			this.authVoteElectionForm.ID = '';
		},

		clearVoteScreen() {
			this.votingSession.DigitsQuantity = 0;
			this.votingSession.VoteChoice = '';
			this.votingSession.Screen = '';
			this.votingSession.candidate.Name = '';
			this.votingSession.candidate.Party = '';
			this.postVote = [];
			this.digits = [];
			this.steps = [];
		},

		swapStage() {
			this.votingSession.Screen = this.electionData[0].Nome;
			this.votingSession.DigitsQuantity = this.electionData[0].Digitos;
			this.votingSession.VoteChoice = '';
			this.votingSession.candidate.Name = '';
			this.votingSession.candidate.Party = '';
		},

		inProgress(election) {
			
			let start = election.StartDate.split('/')
			let beginDate = `${start[2]}-${start[1]}-${start[0]}T${election.StartTime}`;

			let end = election.EndDate.split('/')
			let endDate = `${end[2]}-${end[1]}-${end[0]}T${election.EndTime}`;

			if (new Date(beginDate) <= new Date() && new Date(endDate) >= new Date()) 
				return true;
			else 
				return false;
		},

		onSubmitAuth(e) {
			e.preventDefault();
			const payload = {
				ElectionID: this.authVoteElectionForm.ElectionID,
				ID: this.authVoteElectionForm.ID.replace(/[-.]/g, ''),
				Password: this.authVoteElectionForm.Password
			};
			this.authenticateBoardMember(payload);
			this.clearPswd();
		},

		onResetAuth(e) {
			e.preventDefault();
			this.$refs.authenticateVote.hide();
			this.clearPswd();
		},

		authenticateBoardMember(payload) {
			const path = 'http://localhost:5000/voting';
			axios.post(path, payload)
			.then((res) => {

				let passwordInput = document.getElementById('form-auth-pswd-input');
				let voterInput = document.getElementById('form-auth-id-input');
				
				if (res.data['status'] == 'success' && res.data['Voter'] == 'Enabled') 
				{
					this.electionData = res.data['Roles'];
					this.voteID = payload.ID;
					this.votingSession.Screen = this.electionData[0].Nome;
					this.votingSession.DigitsQuantity = this.electionData[0].Digitos;
					this.$refs.authenticateVote.hide();
					this.$refs.votingModal.show();
				} 
				else if (res.data['status'] == 'success' && res.data['Voter'] == 'Disabled') 
				{
					this.setSuccessFor(passwordInput);
					this.setErrorFor(voterInput, 'Voter already voted.');
				}
				else if (res.data['status'] == 'success' && res.data['Voter'] == 'Ghost')
				{
					this.setSuccessFor(passwordInput);
					this.setErrorFor(voterInput, 'Voter not registered.');
				}
				else if (res.data['status'] == 'failed' && res.data['Voter'] == 'Enabled')
				{
					this.setErrorFor(passwordInput, 'Incorrect password.');
					this.setSuccessFor(voterInput);
				}
				else if (res.data['status'] == 'failed' && res.data['Voter'] == 'Disabled')
				{
					this.setErrorFor(passwordInput, 'Incorrect password.');
					this.setErrorFor(voterInput, 'Voter already voted.');
				}
				else if (res.data['status'] == 'failed' && res.data['Voter'] == 'Ghost')
				{
					this.setErrorFor(passwordInput, 'Incorrect password.');
					this.setErrorFor(voterInput, 'Voter not registered.');
				}
			})
			.catch((err) => {
				alert(err);
				this.getElections();
			});
		},

		checkCandidate(payload) {
			const path = 'http://localhost:5000/voting';
			axios.post(path, payload)
			.then((res) => {
				return res.data['Name'];
			})
			.catch((err) => {
				alert(err);
				this.getElections();
			});
		},
		
		addNumber(digit) {
		
			let audio = new Audio(keyAudio);
			audio.play();

			if (this.votingSession.VoteChoice.length == this.votingSession.DigitsQuantity)
				return false;
			
			this.votingSession.VoteChoice += String(digit);

			// const payload = {
			// 	ID: this.voteID,
			// 	Role: this.votingSession.Screen,
			// 	Choice: this.votingSession.VoteChoice
			// }
			
			// let candName = this.checkCandidate(payload);
			// if (candName != '')
			// 	this.votingSession.candidate.Name = candName;

		},

		blankVote() {
			let audio = new Audio(keyAudio);
			audio.play();

			this.postVote.push('');
			this.electionData.shift();
			
			this.swapStage();
		},

		reviseVote() {
			
			let audio = new Audio(keyAudio);
			audio.play();

			this.votingSession.VoteChoice = '';
			this.votingSession.candidate.Name = '';
			this.votingSession.candidate.Party = '';
		},

		confirmVote() {

			if (this.votingSession.VoteChoice.length < this.votingSession.DigitsQuantity) {
				alert('Vote field incomplete!');
				return false;
			}

			let stepSize = this.steps.length - 1;
			this.digits.push(this.votingSession.DigitsQuantity);

			if (this.digits.length == 0) 
				this.steps.push(this.votingSession.DigitsQuantity);
			else 
				this.steps.push(this.steps[stepSize] + this.votingSession.DigitsQuantity);	

			this.electionData.shift();
			let audio = new Audio(confirmAudio);
			audio.play();

			this.postVote.push(this.votingSession.VoteChoice);

			if (this.electionData.length == 0) {
				alert(this.postVote);
				this.clearVoteScreen();
				this.votingSession.Screen = 'end';

				// const payload = {
				// 	ID: this.voteID,
				// 	Choice: this.postVote,
				// 	Digits: this.digits,
				// 	Steps: this.steps
				// }

				// const path = 'http://localhost:5000/voting';
				// axios.post(path, payload)
				// .then((res) => {
				// 	console.log(res.data);
				// })
				// .catch((err) => {
				// 	alert(err);
				// 	this.getElections();
				// });
				return false;
			}

			this.swapStage();
		},

		setErrorFor(field, message) {

			let formControl = field.parentElement;
			let small = formControl.querySelector('b-small');

			formControl.className = 'create-form-control error';
			small.innerText = message;
		},

		setSuccessFor(field) {

			let formControl = field.parentElement;
			formControl.className = 'create-form-control success';

			setTimeout(function() {
				formControl.className = 'create-form-control';
			}, 2500);
		},

		informElection(election) {
			this.authVoteElectionForm.ElectionID = election.ID;
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
.jumbotron {
	position: absolute;
	width: 90%;
	left: 5%;
}
.vote {
	text-align: center;
	font-size: 30px;
	position: absolute;
	left: 37%;
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
h1 {
	text-align: center;
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
button:hover {
	opacity: 0.8;
}
.vue-otp-2 {
	display: center;
	margin: 0 auto;
	width: 20%;
}
.otp-input {
	width: 20%;
	justify-content: center;
    padding: 5px;
    margin: 0 auto;
    font-size: 20px;
    text-align: center;
}
.otp-input::-webkit-inner-spin-button,
.otp-input::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
}
/* Error messages and styling on inputs */
.create-form-control .exclamation {
	visibility: hidden;
}
.create-form-control.error .exclamation {
	color: #e74c3c;
	position: relative;
	bottom: 33px;
	left: 228px;
	visibility: visible;
}
.create-form-control .check {
	visibility: hidden;
}
.create-form-control.success .check {
	color: #73ff00;
	position: relative;
	bottom: 33px;
	left: 206px;
	visibility: visible;
}
.create-form-control.success input {
	border: 2px solid #73ff00;
}
.create-form-control.error input {
	border: 2px solid #e74c3c;
}
.create-form-control b-small {
	font-size: 14px;
	position: absolute;
	left: 5%;
	margin-top: 5px;
	visibility: hidden;
}
.create-form-control.error b-small {
	color: #ff0000;
	visibility: visible;
}

.urna-tela {
	margin: 0 auto;
	width: 55%;
	height: 100%;
	background-color: #ffffff;
	border-radius: 5px;
	border: 2px solid #000000;
	padding: 20px;
	color: #000000;
}
.urna-tela-voto {
	text-align: center;
	display: flex;
	flex-wrap: wrap;
	width: 100%;
	height: 100%;
}
.urna-tela-voto-textos {
	margin: 0 auto;
}
.urna-tela-voto-titulo {
	font-weight: bold;
	font-size: 20px;
}
.each-number {
	text-align: center;
	display: flex;
	align-items: center;
}
.otp-box {
	width: 45px;
	height: 55px;
	border: 1px solid #000000;
	margin-left: 10px;
	display: flex;
	justify-content: center;
	align-items: center;
	font-size: 30px;
}
.urna-tela-voto-descricao {
	margin-top: 20px;
	font-size: 18px;
}
.urna-tela-voto-imagem img {
	width: 110px;
	height: 150px;
	border: 1px solid #000000;
}
.urna-tela-voto-instrucoes {
	width: 100%;
	border-top: 1px solid #000000;
	font-size: 13px;
	margin-top: 20px;
	padding-top: 10px;
}
.urna-tela-fim {
	display: flex;
	justify-content: center;
	flex-direction: column;
	align-items: center;
	font-size: 120px;
	width: 100%;
	height: 100%;
}
.urna-tela-fim p {
	font-size: 12px;
}
	@media (max-width: 900px) {
	.urna-tela {
		padding: 15px 18px 15px 18px;
	}
	.urna-tela-voto-titulo {
		font-size: 15px;
	}
	.urna-tela-voto-textos {
		flex: 1;
		font-size: 14px;
	}
	.otp-box {
		width: 20px;
		height: 25px;
		font-size: 20px;
		margin-left: 7px;
	}
	.urna-tela-voto-imagem img {
		width: 70px;
		height: 100px;
	}
	.urna-tela-voto-instrucoes {
		width: 80%;
		font-size: 10px;
		margin-top: 10px;
		padding-top: 5px;
	}
}
</style>