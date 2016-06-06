var MovieCell = React.createClass({
  getInitialState: function() {
    return {
      title: "",
      img_url: "",
      movie_id: ""
    };
  },
  _getNewMovie: function() {
    $.ajax({
      url: '/get_movie/' + this.props.user_id,
      dataType: 'json',
      success: function(data) {
        this.setState(data);

      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    })
  },
  componentDidMount: function() {
    this._getNewMovie();
  },
  _ratingOnChange: function(rating) {
    $.ajax({
      url: '/rate/' + this.props.user_id + '/' + this.state.movie_id +'/',
      type: 'POST',
      dataType: 'json',
      data: {'rating': rating},
      success: function(data) {
        this._getNewMovie();
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    })
  },
  render: function() {
    var image_url = this.state.img_url;
    if(!image_url || image_url === "") {
      image_url = "http://i.imdb.com/images/nopicture/140x209/unknown.png";
    }
    console.log(image_url)
    return (
      <div>
      <a href={'/movie/' + this.state.movie_id}>
      <h4>{this.state.title}</h4>
      <img style={{height: '268px', width: '182px'}} src={image_url} />
      </a>
<IconRating onChange={this._ratingOnChange}
  toggledClassName="fa-2x fa fa-star " untoggledClassName="fa-2x fa fa-star-o"/>

      </div>
    );
  }

});

var Movie = React.createClass({
  render: function() {
    return (
      <div>
      <MovieCell user_id={this.props.user_id}/>
      <MovieCell user_id={this.props.user_id}/>
      </div>
    );
  }
});


ReactDOM.render(
  <Movie user_id={myUserId}/>,
  document.getElementById('movie')
);