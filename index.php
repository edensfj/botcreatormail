<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title></title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.8.0/css/bulma.css">
  </head>
  <body>

<div class="table-container">
    <table class="is-bordered is-fullwidth is-hoverable is-narrow is-size-7 is-striped table" >
      <thead>
      <tr>
        <th>ID</th>
        <th>username</th>
        <th>password</th>
        <th>email</th>
        <th>telefono</th>
        <th>validado</th>
        <th>accion</th>
      </tr>
    </thead>
    <tbody>
      </tbody>
    <?php
    $servername = "puntoquimico.com.co";
    $username = "bot";
    $password = md5("bot");
    $dbname = "bot";

    // Create connection
    $conn = new mysqli($servername, $username, $password, $dbname);
    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }


    if (isset($_POST['telefono'],$_POST['id'])) {
      $tel = $_POST['telefono'];
      $id = $_POST['id'];
      $result = $conn->query("UPDATE instagram SET telefono='$tel', validate='1' WHERE id='$id';");
    }



    $sql = "SELECT ins.*,e.email FROM instagram ins inner join emails e on e.id=ins.usedby";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc()) {
?>
          <tr>
            <td><?=$row["id"]?></td>
            <td>
              <a onclick="vercuenta();">
                <?=$row["username"]?>
              </a>
              <!-- <a target="_blank" href="https://www.instagram.com/accounts/login/">
                <?=$row["username"]?>
              </a> -->
            </td>
            <td><?=$row["password"]?></td>
            <td><?=$row["email"]?></td>
            <td><?=$row["telefono"]?></td>
            <td><?=$row["validate"]?></td>
            <td><?php if (!intval($row["validate"])): ?>
              <form class="" action="" method="post">
                <div class="field has-addons">
                  <div class="control">
                    <input type="hidden" name="id" value="<?=$row["id"]?>">
                    <input class="input is-small" type="text" name="telefono" placeholder="numero de telefono">
                  </div>
                  <div class="control"><input type="submit" class="button is-primary is-small" value="Validar"></div>
                </div>
              </form>
            <?php endif; ?></td>
          </tr>
          <?php
        }
    } else {
        echo "0 results";
    }
    $conn->close();
    ?>
  </table>
</div>


<script type="text/javascript">
function vercuenta(){
  var theWindow = window.open('https://www.instagram.com/accounts/login/'),
  theDoc = theWindow.document,
  theScript = document.createElement('script');
  function injectThis() {
    alert("hola mundo");
  }
  theScript.innerHTML = 'window.onload = ' + injectThis.toString() + ';';
  theDoc.body.appendChild(theScript);
}
</script>



  </body>
</html>
