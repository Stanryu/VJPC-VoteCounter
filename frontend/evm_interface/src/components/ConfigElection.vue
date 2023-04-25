<template>
    <div class="container">
		<div class="jumbotron vertical-center">
			
			<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/lux/bootstrap.min.css" 
			integrity="sha384-9+PGKSqjRdkeAU7Eu4nkJU8RFaH8ace8HGXnkiKMP9I9Te0GJ4/km3L1Z8tXigpG" crossorigin="anonymous">
			
			<!-- Election Configuration Main Page -->
			<div class="row">
				<div class="col-sm-12">
					<h2 class="text-center bg-primary text-white">Set Up an Election</h2>
					<hr>
					
					<!-- Feedback Status on the Operation (Create, Edit and Delete) -->
					<b-alert variant="success" v-if="showMessage" show fade dismissible>{{ message }}</b-alert>
					<br>
					
					<button type="button" class="btn btn-success" v-b-modal.election-modal>Create Election</button>
					<br><br>
					
					<hr>
					<h4 class="text-center bg-primary text-white">Upcoming</h4>
					<hr>
					<!-- Contens of Each Election Displayed on a Table Format -->
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
							<tr v-if="upcoming(election)">
								<td>{{ election.Name }}</td>
								<td>{{ election.Description }}</td>
								<td>{{ election.Quantity }}</td>
								<td>{{ election.StartDate }}<br>{{ election.StartTime }}</td>
								<td>{{ election.EndDate }}<br>{{ election.EndTime }}</td>
								<td>{{ election.Fingerprint }}</td>
								<td>
									<div class="btn-group" role="group"> 
										<button type="button" class="btn btn-info btn-sm" 
										:disabled="isManageable(election)" @click="editElection(election)">Update</button>
										<button type="button" class="btn btn-danger btn-sm" 
										:disabled="isManageable(election)" @click="deleteElection(election)">Delete</button>
									</div>
								</td>
							</tr>
						</tbody>
					</table>

					<hr><hr>
					<h4 class="text-center bg-success text-white">In Progress</h4>
					<hr>
					
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
								<td>{{ election.StartDate }}<br>{{ election.StartTime }}</td>
								<td>{{ election.EndDate }}<br>{{ election.EndTime }}</td>
								<td>{{ election.Fingerprint }}</td>
								<td>
									<div class="btn-group" role="group"> 
										<button type="button" class="btn btn-info btn-sm" 
										:disabled="isManageable(election)" @click="editElection(election)">Update</button>
										<button type="button" class="btn btn-danger btn-sm" 
										:disabled="isManageable(election)" @click="deleteElection(election)">Delete</button>
									</div>
								</td>
							</tr>
						</tbody>
					</table>

					<hr><hr>
					<h4 class="text-center bg-danger text-white">Closed</h4>
					<hr>
					
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
							<tr v-if="closed(election)">
								<td>{{ election.Name }}</td>
								<td>{{ election.Description }}</td>
								<td>{{ election.Quantity }}</td>
								<td>{{ election.StartDate }}<br>{{ election.StartTime }}</td>
								<td>{{ election.EndDate }}<br>{{ election.EndTime }}</td>
								<td>{{ election.Fingerprint }}</td>
								<td>
									<div class="btn-group" role="group"> 
										<button type="button" class="btn btn-info btn-sm" 
										:disabled="isManageable(election)" @click="editElection(election)">Update</button>
										<button type="button" class="btn btn-danger btn-sm" 
										:disabled="isManageable(election)" @click="deleteElection(election)">Delete</button>
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

			<!-- Creating Elections Modal -->
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

					<b-form-group class="create-form-control" id="form-startdate-group" label="Start" label-for="form-startdate-input">
						<b-form-input id="form-begindate-input"
									type="datetime-local"
									:min="min"
									v-model="createElectionForm.Start"
									required>
						</b-form-input>
						<span class="exclamation">
							<font-awesome-icon icon="fas fa-exclamation-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<span class="check">
							<font-awesome-icon icon="fas fa-check-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<b-small></b-small>
					</b-form-group>

					<b-form-group class="create-form-control" id="form-enddate-group" label="End" label-for="form-enddate-input">
						<b-form-input id="form-enddate-input" 
									type="datetime-local"
									:min="min"
									v-model="createElectionForm.End" 
									required>
						</b-form-input>
						<span class="exclamation">
							<font-awesome-icon icon="fas fa-exclamation-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<span class="check">
							<font-awesome-icon icon="fas fa-check-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<b-small></b-small>
					</b-form-group>

					<b-form-group class="create-form-control" id="form-password-group" label="Master Password" label-for="form-password-input">
						<b-form-input id="form-password-input" 
									type="password" 
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
						<br><br><br><br><br>
					</b-form-group>

					<b-form-group class="create-form-control" id="form-c-password-group" label="Confirm Password" label-for="form-c-password-input">
						<b-form-input id="form-c-password-input" 
									type="password" 
									v-model="createElectionForm.ConfirmPassword" 
									required 
									placeholder="Confirm the board member master password...">
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
			
			<!-- Editing Elections Modal -->
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

					<b-form-group class="create-form-control" id="form-begindate-edit-group" label="Start" label-for="form-begindate-edit-input">
						<b-form-input id="form-begindate-edit-input" 
									type="datetime-local"
									:min="min"
									v-model="editElectionForm.Start"
									required>
						</b-form-input>
						<span class="exclamation">
							<font-awesome-icon icon="fas fa-exclamation-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<span class="check">
							<font-awesome-icon icon="fas fa-check-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<b-small></b-small>
					</b-form-group>

					<b-form-group class="create-form-control" id="form-enddate-edit-group" label="End" label-for="form-enddate-edit-input">
						<b-form-input id="form-enddate-edit-input" 
							type="datetime-local"
									:min="min"
									v-model="editElectionForm.End"
									required>
						</b-form-input>
						<span class="exclamation">
							<font-awesome-icon icon="fas fa-exclamation-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<span class="check">
							<font-awesome-icon icon="fas fa-check-circle" style="height: 20px;"></font-awesome-icon>
						</span>
						<b-small></b-small>
					</b-form-group>

					<b-form-group class="create-form-control" id="form-password-edit-group" label="Master Password" label-for="form-password-edit-input">
						<b-form-input id="form-password-edit-input" 
									type="password" 
									v-model="editElectionForm.Password" 
									required 
									placeholder="Enter the board member master password...">
						</b-form-input>
						<span class="exclamation">
							<font-awesome-icon icon="fas fa-exclamation-circle" style="height: 18px;"></font-awesome-icon>
						</span>
						<span class="check">
							<font-awesome-icon icon="fas fa-check-circle" style="height: 18px;"></font-awesome-icon>
						</span>
						<b-small></b-small>
						<br><br><br><br><br>
					</b-form-group>

					<b-form-group class="create-form-control" id="form-c-password-edit-group" label="Confirm Password" label-for="form-c-password-edit-input">
						<b-form-input id="form-c-password-edit-input" 
									type="password" 
									v-model="editElectionForm.ConfirmPassword" 
									required 
									placeholder="Confirm the board member master password...">
						</b-form-input>
						<span class="exclamation">
							<font-awesome-icon icon="fas fa-exclamation-circle" style="height: 18px;"></font-awesome-icon>
						</span>
						<span class="check">
							<font-awesome-icon icon="fas fa-check-circle" style="height: 18px;"></font-awesome-icon>
						</span>
						<b-small></b-small>
					</b-form-group>

					<b-button type="submit" variant="outline-info">Submit</b-button>
					<b-button type="reset" variant="outline-danger">Cancel</b-button>
				</b-form>
			</b-modal>

			<!-- Authentication -->
			<b-modal ref="authenticate" id="authenticate" title="Authentication" hide-backdrop hide-footer>
				<b-form @submit="onSubmitAuth" @reset="onResetAuth" class="w-100 text-center">
					
					<b-form-group class="create-form-control" id="form-auth-group" label="Password" label-for="form-auth-input">
						<b-form-input id="form-auth-input" 
									type="password" 
									v-model="authElectionForm.Password" 
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

					<b-button type="submit" variant="outline-success">Authenticate</b-button>
					<b-button type="reset" variant="outline-danger">Cancel</b-button>

				</b-form>
			</b-modal>

		</div>
    </div>
</template>

<script>
import axios from 'axios';

export default 
{
	data() 
	{
		const now = new Date();
		const year = now.getFullYear();
		const month = String(now.getMonth() + 1).padStart(2, '0');
		const day = String(now.getDate()).padStart(2, '0');

		return {
			elections: [],
			createElectionForm: 
			{
				'Name': '',
				'Description': '',
				'CandidatesFile': '',
				'VotersFile': '',
				'Start': '',
				'End': '',
				'Password': '',
				'ConfirmPassword': ''
			},
			editElectionForm: 
			{
				'ID': '',
				'Name': '',
				'Description': '',
				'CandidatesFile': '',
				'VotersFile': '',
				'Start': '',
				'End': '',
				'Password': '',
				'ConfirmPassword': ''
			},
			authElectionForm: 
			{
				'Password': ''
			},
			toRemove: 
			{
				'ID': '',
				'Operation': ''
			},
			min: `${year}-${month}-${day} 00:00`,
			strength: ['- 8 characters',
			'- One number',
			'- One uppercase letter',
			'- One special character'
			]
		};
	},
	message: '',
	methods: {
		getElections() 
		{
			const path = 'http://localhost:5000';
			axios.get(path)
			.then((res) => {
				this.elections = res.data.elections;
			})
			.catch((err) => {
				alert(err);
			});
		},

		createElection(payload) 
		{
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

		clearForm() 
		{
			this.createElectionForm.Name = '';
			this.createElectionForm.Description = '';
			this.createElectionForm.CandidatesFile = '';
			this.createElectionForm.VotersFile = '';
			this.createElectionForm.Start = '';
			this.createElectionForm.End = '';
			this.createElectionForm.Password = '';
			this.createElectionForm.ConfirmPassword = '';
			this.editElectionForm.ID = '';
			this.editElectionForm.Name = '';
			this.editElectionForm.Description = '';
			this.editElectionForm.CandidatesFile = '';
			this.editElectionForm.VotersFile = '';
			this.editElectionForm.Start = '';
			this.editElectionForm.End = '';
			this.editElectionForm.Password = '';
			this.editElectionForm.ConfirmPassword = '';
		},

		clearAuthPswd() 
		{
			this.authElectionForm.Password = '';
		},

		// clearRemoved() 
		// {
		// 	this.toRemove.ID = '';
		// 	this.toRemove.Operation = '';
		// },

		checkInputs(modus) 
		{

			let startInput, endInput, passwordInput, confirmPasswordInput;

			if (modus == 'create') 
			{
				startInput = document.getElementById('form-begindate-input');
				endInput = document.getElementById('form-enddate-input');
				passwordInput = document.getElementById('form-password-input');
				confirmPasswordInput = document.getElementById('form-c-password-input');

				let beginDate = new Date(this.createElectionForm.Start);
				let endDate = new Date(this.createElectionForm.End);

				if (beginDate.getTime() >= endDate.getTime()) 
				{
					this.setErrorFor(startInput, "Start date must be before the end.");
					this.setErrorFor(endInput, "End date must be after the beginning.");
				} 
				else if (beginDate.getTime() <= new Date()) 
				{
					this.setErrorFor(startInput, "Start date must be in the future.");
					this.setErrorFor(endInput, "End date must be in the future.");
				} 
				else 
				{
					this.setSuccessFor(startInput);
					this.setSuccessFor(endInput);
				}

				let warning = '';
				let weakPswd = false;
				let checkStrength = this.passwordStrength(this.createElectionForm.Password);

				for (let x = 0; x < checkStrength.length; x++) 
				{
					if (!checkStrength[x]) {
						weakPswd = true;
						warning = `${warning}\n${this.strength[x]}`
					}
				}

				if (weakPswd && this.createElectionForm.Password != this.createElectionForm.ConfirmPassword)
				{
					this.setErrorFor(passwordInput, `Password must have at least:${warning}`);
					this.setErrorFor(confirmPasswordInput, "Passwords don't match.");
				}
				else if (weakPswd && this.createElectionForm.Password == this.createElectionForm.ConfirmPassword) 
				{
					this.setErrorFor(passwordInput, `Password must have at least:${warning}`);
					this.setErrorFor(confirmPasswordInput, '');
				}
				else if (!weakPswd && this.createElectionForm.Password != this.createElectionForm.ConfirmPassword) 
				{
					this.setErrorFor(passwordInput, '');
					this.setErrorFor(confirmPasswordInput, "Passwords don't match.");
				} 
				else 
				{
					this.setSuccessFor(passwordInput);
					this.setSuccessFor(confirmPasswordInput);
				}
			} 
			else if (modus == 'edit') 
			{
				
				startInput = document.getElementById('form-begindate-edit-input');
				endInput = document.getElementById('form-enddate-edit-input');
				passwordInput = document.getElementById('form-password-edit-input');

				let beginDate = new Date(this.editElectionForm.Start);
				let endDate = new Date(this.editElectionForm.End);
				
				if (beginDate.getTime() >= endDate.getTime()) 
				{
					this.setErrorFor(startInput, "Start date must be before the end.");
					this.setErrorFor(endInput, "End date must be after the beginning.");
				} 
				else if (beginDate.getTime() <= new Date()) 
				{
					this.setErrorFor(startInput, "Start date must be in the future.");
					this.setErrorFor(endInput, "End date must be in the future.");
				} 
				else 
				{
					this.setSuccessFor(startInput);
					this.setSuccessFor(endInput);
				}

				let warning = '';
				let weakPswd = false;
				let checkStrength = this.passwordStrength(this.editElectionForm.Password);

				for (let x = 0; x < checkStrength.length; x++) 
				{
					if (!checkStrength[x]) {
						weakPswd = true;
						warning = `${warning}\n${this.strength[x]}`
					}
				}

				if (weakPswd && this.editElectionForm.Password != this.editElectionForm.ConfirmPassword)
				{
					this.setErrorFor(passwordInput, `Password must have at least:${warning}`);
					this.setErrorFor(confirmPasswordInput, "Passwords don't match.");
				}
				else if (weakPswd && this.editElectionForm.Password == this.editElectionForm.ConfirmPassword) 
				{
					this.setErrorFor(passwordInput, `Password must have at least:${warning}`);
					this.setErrorFor(confirmPasswordInput, '');
				}
				else if (!weakPswd && this.editElectionForm.Password != this.editElectionForm.ConfirmPassword) 
				{
					this.setErrorFor(passwordInput, '');
					this.setErrorFor(confirmPasswordInput, "Passwords don't match.");
				} 
				else 
				{
					this.setSuccessFor(passwordInput);
					this.setSuccessFor(confirmPasswordInput);
				}
			}

			const formControls = document.querySelectorAll('.create-form-control');

			const formIsValid = [...formControls].every(formControl => {
				return (formControl.className != 'create-form-control error');
			});

			return formIsValid;
		},

		passwordStrength(password) 
		{
			let minLength = password.length > 7;
			let hasDigit = /\d/.test(password);
			let hasUpperCase = /[A-Z]/.test(password);
			let hasSpecial = /[!~"'´`ªº?\\|/><,;{}¨§£¢¬@#$%^&*)\][(+=._-]/.test(password);

			return [minLength, hasDigit, hasUpperCase, hasSpecial];
		},

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

		onSubmit(e) {
			e.preventDefault();
			
			let check = this.checkInputs('create');
			
			if (check) {
				this.$refs.createElectionModal.hide();

				// Date original format --> yyyy-mm-ddTHH:mm
				let beginDate = new Date(this.createElectionForm.Start).toLocaleDateString('pt-BR');
				let endDate = new Date(this.createElectionForm.End).toLocaleDateString('pt-BR');
				let beginTime = this.createElectionForm.Start.split('T')[1];
				let endTime = this.createElectionForm.End.split('T')[1];

				const payload = {
					Name: this.createElectionForm.Name,
					Description: this.createElectionForm.Description,
					CandidatesFile: this.createElectionForm.CandidatesFile,
					VotersFile: this.createElectionForm.VotersFile,
					StartDate: beginDate,
					StartTime: beginTime,
					EndDate: endDate,
					EndTime: endTime,
					Password: this.createElectionForm.Password
				};
				this.createElection(payload);
				this.clearForm();
			}
		},

		onReset(e) {
			e.preventDefault();
			this.$refs.createElectionModal.hide();
			this.clearForm();
			this.getElections();
		},

		onSubmitAuth(e) {
			e.preventDefault();
			const payload = {
				ID: this.toRemove.ID,
				Password: this.authElectionForm.Password
			};
			this.authenticateBoardMember(payload);
			this.clearAuthPswd();
		},

		onResetAuth(e) {
			e.preventDefault();
			this.$refs.authenticate.hide();
			this.clearAuthPswd();
			this.getElections();
		},

		onSubmitUpdate(e) {
			e.preventDefault();
			
			let check = this.checkInputs('edit');
			
			if (check) {
				this.$refs.editElectionModal.hide();

				let beginDate = new Date(this.editElectionForm.Start).toLocaleDateString('pt-BR');
				let endDate = new Date(this.editElectionForm.End).toLocaleDateString('pt-BR');
				let beginTime = this.editElectionForm.Start.split('T')[1];
				let endTime = this.editElectionForm.End.split('T')[1];

				const payload = {
					Name: this.editElectionForm.Name,
					Description: this.editElectionForm.Description,
					CandidatesFile: this.editElectionForm.CandidatesFile,
					VotersFile: this.editElectionForm.VotersFile,
					StartDate: beginDate,
					StartTime: beginTime,
					EndDate: endDate,
					EndTime: endTime,
					Password: this.editElectionForm.Password
				};
				this.updateElection(payload, this.editElectionForm.ID);
				this.clearForm();
			}
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
				
				if (res.data['status'] == 'success') {
					this.$refs.authenticate.hide();
					
					if (this.toRemove.Operation == 'D')
						this.removeElection(this.toRemove.ID);
					else 
						this.$refs.editElectionModal.show();
				} else {
					let passwordInput = document.getElementById('form-auth-input');
					this.setErrorFor(passwordInput, 'Incorrect Password.');
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
			
			let splitDate = election.StartDate.split('/')
			let formattedDate = `${splitDate[2]}-${splitDate[1]}-${splitDate[0]}T${election.StartTime}`;

			if (new Date(formattedDate) > new Date()) {
				this.editElectionForm = election;
				this.toRemove.ID = election.ID;
				this.toRemove.Operation = '';
				this.$refs.authenticate.show();
			} else
				this.getElections();
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

			let splitDate = election.StartDate.split('/')
			let formattedDate = `${splitDate[2]}-${splitDate[1]}-${splitDate[0]}T${election.StartTime}`;

			if (new Date(formattedDate) > new Date()) {
				this.toRemove.ID = election.ID;
				this.toRemove.Operation = 'D';
				this.$refs.authenticate.show();
			} else
				this.getElections();
		},

		isManageable(election) {

			let splitDate = election.StartDate.split('/')
			let formattedDate = `${splitDate[2]}-${splitDate[1]}-${splitDate[0]}T${election.StartTime}`;

			if (new Date(formattedDate) <= new Date()) 
				return true;
			else 
				return false;
		},

		upcoming(election) {

			let splitDate = election.StartDate.split('/')
			let formattedDate = `${splitDate[2]}-${splitDate[1]}-${splitDate[0]}T${election.StartTime}`;

			if (new Date(formattedDate) > new Date()) 
				return true;
			else 
				return false;
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

		closed(election) {

			let end = election.EndDate.split('/')
			let endDate = `${end[2]}-${end[1]}-${end[0]}T${election.EndTime}`;

			if (new Date(endDate) < new Date()) 
				return true;
			else 
				return false;
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
h4 {
	margin: 0 auto;
	padding: 10px;
	width: 20%;
	border-radius: 5px;
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
.jumbotron {
	position: absolute;
	width: 90%;
	left: 5%;
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
</style>
