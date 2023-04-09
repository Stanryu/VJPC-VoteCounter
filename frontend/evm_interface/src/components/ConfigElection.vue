<template>
    <div class="container">
		<div class="jumbotron vertical-center">
			
			<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/lux/bootstrap.min.css" 
			integrity="sha384-9+PGKSqjRdkeAU7Eu4nkJU8RFaH8ace8HGXnkiKMP9I9Te0GJ4/km3L1Z8tXigpG" crossorigin="anonymous">
			
			<div class="row">
				<div class="col-sm-12">
					<h2 class="text-center bg-primary text-white">Set Up an Election</h2>
					<hr><br>
					
					<b-alert variant="success" v-if="showMessage" show fade dismissible>{{ message }}</b-alert>
					<br>
					
					<button type="button" class="btn btn-success btn-sm" v-b-modal.election-modal>Create Election</button>
					<br><br>
					
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
										<button type="button" class="btn btn-info btn-sm" v-b-modal.authenticate-edit @click="editElection(election)">Update</button>
										<button type="button" class="btn btn-danger btn-sm" v-b-modal.authenticate-edit @click="deleteElection(election)">Delete</button>
									</div>
								</td>
							</tr>
						</tbody>
					</table>
					<footer class="bg-primary text-white text-center" style="border-radius: 10px;">Copyright &copy;. All Rights Reserved 2023.</footer>
				</div>
			</div>

			<b-modal ref="createElectionModal" id="election-modal" title="Create a New Election" hide-backdrop hide-footer>
				<b-form @submit="onSubmit" @reset="onReset" class="w-100 text-center">

					<b-form-group id="form-name-group" label="Name" label-for="form-name-input">
						<b-form-input id="form-name-input" 
									type="text" 
									v-model="createElectionForm.Name" 
									required 
									placeholder="Enter the election name...">
						</b-form-input>
					</b-form-group>

					<b-form-group id="form-description-group" label="Description" label-for="form-description-input">
						<b-form-input id="form-description-input" 
									type="text" 
									v-model="createElectionForm.Description" 
									required 
									placeholder="Enter the election description...">
						</b-form-input>
					</b-form-group>

					<b-form-group class="create-form-control" id="form-begindate-group" label="Start Date" label-for="form-begindate-input">
						<b-form-input id="form-begindate-input" 
									type="text" 
									v-model="createElectionForm.StartDate" 
									required 
									placeholder="Enter the election start date... (e.g., dd/MM/yyyy)">
						</b-form-input>
						<span class="exclamation">
							<font-awesome-icon icon="fas fa-exclamation-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<span class="check">
							<font-awesome-icon icon="fas fa-check-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<b-small></b-small>
					</b-form-group>

					<b-form-group class="create-form-control" id="form-starttime-group" label="Start Time" label-for="form-starttime-input">
						<b-form-input id="form-starttime-input" 
									type="text" 
									v-model="createElectionForm.StartTime" 
									required 
									placeholder="Enter the election start time... (e.g., hh:mm)">
						</b-form-input>
						<span class="exclamation">
							<font-awesome-icon icon="fas fa-exclamation-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<span class="check">
							<font-awesome-icon icon="fas fa-check-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<b-small></b-small>
					</b-form-group>

					<b-form-group class="create-form-control" id="form-enddate-group" label="End Date" label-for="form-enddate-input">
						<b-form-input id="form-enddate-input" 
									type="text" 
									v-model="createElectionForm.EndDate" 
									required 
									placeholder="Enter the election end date... (e.g., dd/MM/yyyy)">
						</b-form-input>
						<span class="exclamation">
							<font-awesome-icon icon="fas fa-exclamation-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<span class="check">
							<font-awesome-icon icon="fas fa-check-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<b-small></b-small>
					</b-form-group>

					<b-form-group class="create-form-control" id="form-endtime-group" label="End Time" label-for="form-endtime-input">
						<b-form-input id="form-endtime-input" 
									type="text" 
									v-model="createElectionForm.EndTime" 
									required 
									placeholder="Enter the election end time... (e.g., hh:mm)">
						</b-form-input>
						<span class="exclamation">
							<font-awesome-icon icon="fas fa-exclamation-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<span class="check">
							<font-awesome-icon icon="fas fa-check-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<b-small></b-small>
					</b-form-group>

					<b-form-group id="form-candidatesfile-group" label="Candidates File" label-for="form-candidatesfile-input">
						<b-form-input id="form-candidatesfile-input" 
									type="text" 
									v-model="createElectionForm.CandidatesFile" 
									required 
									placeholder="Enter the candidates file name... ">
						</b-form-input>
					</b-form-group>

					<b-form-group id="form-votersfile-group" label="Voters File" label-for="form-votersfile-input">
						<b-form-input id="form-votersfile-input" 
									type="text" 
									v-model="createElectionForm.VotersFile" 
									required 
									placeholder="Enter the voters file name... ">
						</b-form-input>
					</b-form-group>

					<b-form-group class="create-form-control" id="form-password-group" label="Master Password" label-for="form-password-input">
						<b-form-input id="form-password-input" 
									type="text" 
									v-model="createElectionForm.Password" 
									required 
									placeholder="Enter the board member master password...">
						</b-form-input>
						<span class="exclamation">
							<font-awesome-icon icon="fas fa-exclamation-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<span class="check">
							<font-awesome-icon icon="fas fa-check-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<b-small></b-small>
					</b-form-group>

					<b-button type="submit" variant="outline-info">Submit</b-button>
					<b-button type="reset" variant="outline-danger">Cancel</b-button>
				</b-form>
			</b-modal>

			<b-modal ref="authenticateEdit" id="authenticate-edit" title="Authentication" hide-backdrop hide-footer>
				<b-form @submit="onSubmitAuth" @reset="onResetAuth" class="w-100 text-center">
					
					<b-form-group id="form-auth-edit-group" label="Password" label-for="form-auth-edit-input">
						<b-form-input id="form-auth-edit-input" 
									type="text" 
									v-model="authEditElectionForm.Password" 
									required 
									placeholder="Enter your master password...">
						</b-form-input>
					</b-form-group>

					<b-button type="submit" variant="outline-success">Authenticate</b-button>
					<b-button type="reset" variant="outline-danger">Cancel</b-button>

				</b-form>
			</b-modal>

			<b-modal ref="editElectionModal" id="election-edit-modal" title="Edit an Election" hide-backdrop hide-footer>
				<b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100 text-center">
					
					<b-form-group id="form-name-edit-group" label="Name" label-for="form-name-edit-input">
						<b-form-input id="form-name-edit-input" 
									type="text" 
									v-model="editElectionForm.Name" 
									required 
									placeholder="Enter the election name...">
						</b-form-input>
					</b-form-group>

					<b-form-group id="form-description-edit-group" label="Description" label-for="form-description-edit-input">
						<b-form-input id="form-description-edit-input" 
									type="text" 
									v-model="editElectionForm.Description" 
									required 
									placeholder="Enter the election description...">
						</b-form-input>
					</b-form-group>

					<b-form-group class="create-form-control" id="form-begindate-edit-group" label="Start Date" label-for="form-begindate-edit-input">
						<b-form-input id="form-begindate-edit-input" 
									type="text" 
									v-model="editElectionForm.StartDate" 
									required 
									placeholder="Enter the election start date... (e.g., dd/MM/yyyy)">
						</b-form-input>
						<span class="exclamation">
							<font-awesome-icon icon="fas fa-exclamation-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<span class="check">
							<font-awesome-icon icon="fas fa-check-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<b-small></b-small>
					</b-form-group>

					<b-form-group class="create-form-control" id="form-starttime-edit-group" label="Start Time" label-for="form-starttime-edit-input">
						<b-form-input id="form-starttime-edit-input" 
									type="text" 
									v-model="editElectionForm.StartTime" 
									required 
									placeholder="Enter the election start time... (e.g., hh:mm)">
						</b-form-input>
						<span class="exclamation">
							<font-awesome-icon icon="fas fa-exclamation-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<span class="check">
							<font-awesome-icon icon="fas fa-check-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<b-small></b-small>
					</b-form-group>

					<b-form-group class="create-form-control" id="form-enddate-edit-group" label="End Date" label-for="form-enddate-edit-input">
						<b-form-input id="form-enddate-edit-input" 
									type="text" 
									v-model="editElectionForm.EndDate" 
									required 
									placeholder="Enter the election end date... (e.g., dd/MM/yyyy)">
						</b-form-input>
						<span class="exclamation">
							<font-awesome-icon icon="fas fa-exclamation-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<span class="check">
							<font-awesome-icon icon="fas fa-check-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<b-small></b-small>
					</b-form-group>

					<b-form-group class="create-form-control" id="form-endtime-edit-group" label="End Time" label-for="form-endtime-edit-input">
						<b-form-input id="form-endtime-edit-input" 
									type="text" 
									v-model="editElectionForm.EndTime" 
									required 
									placeholder="Enter the election end time... (e.g., hh:mm)">
						</b-form-input>
						<span class="exclamation">
							<font-awesome-icon icon="fas fa-exclamation-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<span class="check">
							<font-awesome-icon icon="fas fa-check-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<b-small></b-small>
					</b-form-group>

					<b-form-group id="form-candidatesfile-edit-group" label="Candidates File" label-for="form-candidatesfile-edit-input">
						<b-form-input id="form-candidatesfile-edit-input" 
									type="text" 
									v-model="editElectionForm.CandidatesFile" 
									required 
									placeholder="Enter the candidates file name... ">
						</b-form-input>
					</b-form-group>

					<b-form-group id="form-votersfile-edit-group" label="Voters File" label-for="form-votersfile-edit-input">
						<b-form-input id="form-votersfile-edit-input" 
									type="text" 
									v-model="editElectionForm.VotersFile" 
									required 
									placeholder="Enter the voters file name... ">
						</b-form-input>
					</b-form-group>

					<b-form-group class="create-form-control" id="form-password-edit-group" label="Master Password" label-for="form-password-edit-input">
						<b-form-input id="form-password-edit-input" 
									type="text" 
									v-model="editElectionForm.Password" 
									required 
									placeholder="Enter the board member master password...">
						</b-form-input>
						<span class="exclamation">
							<font-awesome-icon icon="fas fa-exclamation-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<span class="check">
							<font-awesome-icon icon="fas fa-check-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<b-small></b-small>
					</b-form-group>

					<b-button type="submit" variant="outline-info">Submit</b-button>
					<b-button type="reset" variant="outline-danger">Cancel</b-button>
				</b-form>
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
			createElectionForm: {
				'Name': '',
				'Description': '',
				'StartDate': '',
				'StartTime': '',
				'EndDate': '',
				'EndTime': '',
				'CandidatesFile': '',
				'VotersFile': '',
				'Password': ''
			},
			editElectionForm: {
				'ID': '',
				'Name': '',
				'Description': '',
				'StartDate': '',
				'StartTime': '',
				'EndDate': '',
				'EndTime': '',
				'CandidatesFile': '',
				'VotersFile': '',
				'Password': ''
			},
			authEditElectionForm: {
				'Password': ''
			},
			toRemove: {
				'ID': '',
				'Operation': ''
			}
		};
	},
	message: '',
	methods: {
		getElections() {
			const path = 'http://localhost:5000';
			axios.get(path)
			.then((res) => {
				this.elections = res.data.elections;
			})
			.catch((err) => {
				alert(err);
			});
		},

		createElection(payload) {
			const path = 'http://localhost:5000';
			axios.post(path, payload)
			.then(() => {
				this.getElections();
				this.message = 'Election Created!';
				this.showMessage = true;
			})
			.catch((err) => {
				alert(err);
				this.getElections();
			});
		},

		clearForm() {
			this.createElectionForm.Name = '';
			this.createElectionForm.Description = '';
			this.createElectionForm.StartDate = '';
			this.createElectionForm.StartTime = '';
			this.createElectionForm.EndDate = '';
			this.createElectionForm.EndTime = ''
			this.createElectionForm.CandidatesFile = '';
			this.createElectionForm.VotersFile = '';
			this.createElectionForm.Password = '';
			this.editElectionForm.ID = '';
			this.editElectionForm.Name = '';
			this.editElectionForm.Description = '';
			this.editElectionForm.StartDate = '';
			this.editElectionForm.StartTime = '';
			this.editElectionForm.EndDate = '';
			this.editElectionForm.EndTime = ''
			this.editElectionForm.CandidatesFile = '';
			this.editElectionForm.VotersFile = '';
			this.editElectionForm.Password = '';
		},

		clearPswd() {
			this.authEditElectionForm.Password = '';
		},

		clearRemoved() {
			this.toRemove.ID = '';
			this.toRemove.Operation = '';
		},

		onSubmit(e) {
			e.preventDefault();
			
			// this.checkInputs('create');
			
			this.$refs.createElectionModal.hide();
			const payload = {
				Name: this.createElectionForm.Name,
				Description: this.createElectionForm.Description,
				StartDate: this.createElectionForm.StartDate,
				StartTime: this.createElectionForm.StartTime,
				EndDate: this.createElectionForm.EndDate,
				EndTime: this.createElectionForm.EndTime,
				CandidatesFile: this.createElectionForm.CandidatesFile,
				VotersFile: this.createElectionForm.VotersFile,
				Password: this.createElectionForm.Password
			};
			this.createElection(payload);
			this.clearForm();
		},

		// checkInputs(modus) {

		// 	let startDateInput, startTimeInput, endDateInput, endTimeInput, passwordInput;
			
		// 	if (modus == 'create') {
		// 		startDateInput = document.getElementById('form-begindate-input');
		// 		startTimeInput = document.getElementById('form-starttime-input');
		// 		endDateInput = document.getElementById('form-enddate-input');
		// 		endTimeInput = document.getElementById('form-endtime-input');
		// 		passwordInput = document.getElementById('form-password-input');
		// 	} else if (modus == 'edit') {
		// 		startDateInput = document.getElementById('form-begindate-edit-input');
		// 		startTimeInput = document.getElementById('form-starttime-edit-input');
		// 		endDateInput = document.getElementById('form-enddate-edit-input');
		// 		endTimeInput = document.getElementById('form-endtime-edit-input');
		// 		passwordInput = document.getElementById('form-password-edit-input');
		// 	}

		// 	if (this.createElectionForm.StartTime == 'test') 
		// 		this.setErrorFor(startTimeInput, 'lorem ipsum heren');
		// },

		setSuccessFor(field) {

			let formControl = field.parentElement;
			formControl.className = 'create-form-control success';

			setTimeout(function() {
				formControl.className = 'create-form-control';
			}, 2500);
		},

		setErrorFor(field, message) {

			let formControl = field.parentElement;
			let small = formControl.querySelector('b-small');

			formControl.className = 'create-form-control error';
			small.innerText = message;
		},

		onReset(e) {
			e.preventDefault();
			this.$refs.createElectionModal.hide();
			this.clearForm();
		},

		onSubmitAuth(e) {
			e.preventDefault();
			const payload = {
				Password: this.authEditElectionForm.Password
			};
			this.authenticateBoardMember(payload);
			this.clearPswd();
		},

		onResetAuth(e) {
			e.preventDefault();
			this.$refs.authenticateEdit.hide();
			this.clearPswd();
		},

		onSubmitUpdate(e) {
			e.preventDefault();
			this.$refs.editElectionModal.hide();
			const payload = {
				Name: this.editElectionForm.Name,
				Description: this.editElectionForm.Description,
				StartDate: this.editElectionForm.StartDate,
				StartTime: this.editElectionForm.StartTime,
				EndDate: this.editElectionForm.EndDate,
				EndTime: this.editElectionForm.EndTime,
				CandidatesFile: this.editElectionForm.CandidatesFile,
				VotersFile: this.editElectionForm.VotersFile,
				Password: this.editElectionForm.Password
			};
			this.updateElection(payload, this.editElectionForm.ID);
			this.clearForm();
		},

		onResetUpdate(e) {
			e.preventDefault();
			this.$refs.editElectionModal.hide();
			this.clearForm();
			this.getElections();
		},

		authenticateBoardMember(payload) {
			const path = 'http://localhost:5000';
			axios.post(path, payload)
			.then((res) => {
				if (res.data['status'] == 'success' && this.toRemove.Operation == '') {
					this.$refs.authenticateEdit.hide();
					this.$refs.editElectionModal.show();
				} else if (res.data['status'] == 'success' && this.toRemove.Operation == 'D') {
					this.$refs.authenticateEdit.hide();
					this.removeElection(this.toRemove.ID);
					this.clearRemoved();
				}
			})
			.catch((err) => {
				alert(err);
				this.getElections();
			});
		},

		updateElection(payload, electionID) {
			const path = `http://localhost:5000/${electionID}`;
			axios.put(path, payload)
			.then(() => {
				this.getElections();
				this.message = 'Election Updated!';
				this.showMessage = true;
			})
			.catch((err) => {
				alert(err);
				this.getElections();
			});
		},

		editElection(election) {
			this.editElectionForm = election;
		},

		removeElection(electionID) {
			const path = `http://localhost:5000/${electionID}`;
			axios.delete(path)
			.then(() => {
				this.getElections();
				this.message = 'Election Removed!';
				this.showMessage = true;
			})
			.catch((err) => {
				alert(err);
				this.getElections();
			});
		},

		deleteElection(election) {
			this.toRemove['ID'] = election.ID;
			this.toRemove['Operation'] = 'D';
		}
	},
	created() {
		this.getElections();
	}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
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
/* Error messages and styling on inputs */
.create-form-control .exclamation {
	visibility: hidden;
}
.create-form-control.error .exclamation {
	color: #e74c3c;
	position: relative;
	bottom: 33px;
	left: 225px;
    visibility: visible;
}
.create-form-control .check {
	visibility: hidden;
}
.create-form-control.success .check {
	color: #73ff00;
	position: relative;
	bottom: 33px;
	left: 200px;
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
	left: 35%;
    margin-top: 5px;
    visibility: hidden;
}
.create-form-control.error b-small {
    color: #ff0000;
    visibility: visible;
}
</style>
